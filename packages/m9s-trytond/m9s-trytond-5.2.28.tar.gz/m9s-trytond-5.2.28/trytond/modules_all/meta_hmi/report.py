# -*- coding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction

from trytond.modules.company import CompanyReport


class NamedFileReport(CompanyReport):

    @classmethod
    def _get_report_name(cls, ids, data):
        pool = Pool()
        ActionReport = pool.get('ir.action.report')

        action_id = data.get('action_id')
        if action_id is None:
            action_reports = ActionReport.search([
                    ('report_name', '=', cls.__name__)
                    ])
            assert action_reports, '%s not found' % cls
            action_report = action_reports[0]
        else:
            action_report = ActionReport(action_id)

        model = action_report.model or data.get('model')
        records = cls._get_records(ids, model, data)
        if records:
            return cls._get_report_filename(records[0])

    @classmethod
    def execute(cls, ids, data):
        # The try: except: is only for the case of the invoice report
        # failing with
        # TypeError: cannot unpack non-iterable NoneType object
        # when doing super()
        try:
            ext, content, direct, name = super(NamedFileReport, cls).execute(
                ids, data)
            name = cls._get_report_name(ids, data)
            return ext, content, direct, name
        except TypeError:
            pass

    @classmethod
    def get_context(cls, records, data):
        report_context = super(NamedFileReport, cls).get_context(records, data)
        report_context['format_tax'] = cls.format_tax
        return report_context

    @classmethod
    def format_tax(cls, value, lang, date=None):
        '''
        Provide a function that returns the description of the used tax(es)
        valid at the date or today.
        '''
        pool = Pool()
        Lang = pool.get('ir.lang')
        Date = pool.get('ir.date')

        if lang is None:
            lang = Lang.get()
        if date is None:
            date = Date.today()
        res = ''
        with Transaction().set_context(language=lang):
            for tax in value:
                if tax.childs:
                    for child in tax.childs:
                        if ((child.start_date and date < child.start_date)
                                or (child.end_date and date > child.end_date)):
                            continue
                        res += child.description
                else:
                    res = tax.description
        return res


class PurchaseReport(NamedFileReport):
    __name__ = 'purchase.purchase'

    @classmethod
    def _get_report_filename(cls, record):
        filename = 'Auftrag_%(party)s'
        if record.number:
            filename += '_%(number)s'
        if record.purchase_date:
            filename += '_%(date)s'
        return filename % {
            'party': record.party.name,
            'number': record.number,
            'date': record.purchase_date,
            }


class PurchaseReportHmiWoPrices(PurchaseReport):
    __name__ = 'purchase.purchase.hmi_wo_prices'


class SaleReport(NamedFileReport):
    __name__ = 'sale.sale'

    @classmethod
    def _get_report_filename(cls, record):
        filename = 'Auftrag_%(party)s'
        if record.number:
            filename += '_%(number)s'
        if record.sale_date:
            filename += '_%(date)s'
        return filename % {
            'party': record.party.name,
            'number': record.number,
            'date': record.sale_date,
            }


class DeliveryNote(NamedFileReport, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.delivery_note'

    @classmethod
    def get_context(cls, records, data):
        '''
        stock
          - Complete override to get proper product names on the delivery note
            We want to use rather the sale line description (that could be
            quite different from the sale line description) than the product
            rec_name when available.
        '''
        report_context = super(DeliveryNote, cls).get_context(records, data)
        report_context['product_name'] = cls.product_name
        return report_context

    @classmethod
    def product_name(cls, move_id, language):
        pool = Pool()
        Product = pool.get('product.product')
        Move = pool.get('stock.move')

        with Transaction().set_context(language=language):
            move = Move(move_id)
            name = Product(move.product).name
        return name

    @classmethod
    def _get_report_filename(cls, record):
        filename = 'Lieferschein_%(party)s'
        if record.number:
            filename += '_%(number)s'
        if record.effective_date:
            filename += '_%(date)s'
        return filename % {
            'party': record.customer.name,
            'number': record.number,
            'date': record.effective_date,
            }


class InvoiceReport(NamedFileReport, metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def _get_report_filename(cls, record):
        if record.total_amount >= Decimal('0.0'):
            filename = 'Rechnung_%(party)s'
        else:
            filename = 'Gutschrift_%(party)s'
        if record.number:
            filename += '_%(number)s'
        if record.invoice_date:
            filename += '_%(date)s'
        return filename % {
            'party': record.party.name,
            'number': record.number,
            'date': record.invoice_date,
            }


class TrialBalance(NamedFileReport, metaclass=PoolMeta):
    __name__ = 'account.trial_balance'

    @classmethod
    def get_context(cls, records, data):
        '''
        account
          - Only show booked accounts in the report
        '''
        report_context = super(TrialBalance, cls).get_context(records, data)

        booked_records = []
        all_records = report_context['records']
        for record in all_records:
            if any([record.start_balance, record.debit, record.credit]):
                booked_records.append(record)
        report_context['accounts'] = booked_records
        return report_context

    @classmethod
    def _get_report_filename(cls, record):
        pool = Pool()
        Date = pool.get('ir.date')
        today = Date.today()

        filename = 'SummenundSaldenliste_%(company)s_%(today)s'
        return filename % {
            'company': record.company.party.name,
            'today': today,
            }

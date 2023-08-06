# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond.pool import PoolMeta
from trytond.model import fields


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    webshop_mail_paid = fields.Function(fields.Boolean('Send Mail on Payment'),
        'get_webshop_mail_paid')

    def get_rec_name(self, name):
        if self.total_amount >= Decimal('0.0'):
            rec_name = 'Rechnung'
        else:
            rec_name = 'Gutschrift'
        rec_name += '-%(party)s'
        if self.state in {'posted', 'paid'}:
            rec_name += '-%(number)s'

        return rec_name % {
            'party': self.party.name,
            'number': self.number,
            }

    @classmethod
    def get_webshop_mail_paid(cls, invoices, name):
        '''
        For use in the evaluation of trigger conditions in email templates.
        '''
        paid_invoices = {}
        for invoice in invoices:
            if (invoice.state == 'paid'
                    and invoice.type == 'out'
                    and invoice.sales[0].channel_type == 'webshop'
                    and invoice.untaxed_amount >= Decimal('0.0')):
                paid_invoices[invoice.id] = True
            else:
                paid_invoices[invoice.id] = False
        return paid_invoices


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @staticmethod
    def default_quantity():
        return 1

    @classmethod
    def _account_domain(cls, type_):
        '''
        Allow to use accounts of type 'other' in invoice lines
          - needed to process contracts with lines, that contain amounts
            not going to be a revenue of the company, but to be forwarded
            to the commissioner (#2452).
        '''
        domain = super(InvoiceLine, cls)._account_domain(type_)
        return domain + [('type.other', '=', True)]

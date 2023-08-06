# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

__all__ = ['Invoice', 'InvoiceTax', 'InvoiceLine']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    different_currencies = fields.Function(
        fields.Boolean('Different Currencies'),
        'on_change_with_different_currencies')
    company_currency_digits = fields.Function(
        fields.Integer('Company Currency Digits'),
        'on_change_with_company_currency_digits')
    company_untaxed_amount_cache = fields.Numeric('Untaxed (Company Currency)',
        digits=(16, Eval('company_currency_digits', 2)), readonly=True,
        depends=['company_currency_digits'])
    company_untaxed_amount = fields.Function(
        fields.Numeric('Untaxed (Company Currency)',
            digits=(16, Eval('company_currency_digits', 2)), states={
                'invisible': ~Eval('different_currencies', False),
                },
            depends=['different_currencies', 'company_currency_digits']),
        'get_amount')
    company_tax_amount_cache = fields.Numeric('Tax (Company Currency)',
        digits=(16, Eval('company_currency_digits', 2)), readonly=True,
        depends=['company_currency_digits'])
    company_tax_amount = fields.Function(
        fields.Numeric('Tax (Company Currency)',
            digits=(16, Eval('company_currency_digits', 2)), states={
                'invisible': ~Eval('different_currencies', False),
                },
            depends=['different_currencies', 'company_currency_digits']),
        'get_amount')
    company_total_amount_cache = fields.Numeric('Total (Company Currency)',
        digits=(16, Eval('company_currency_digits', 2)), readonly=True,
        depends=['company_currency_digits'])
    company_total_amount = fields.Function(
        fields.Numeric('Total (Company Currency)',
            digits=(16, Eval('company_currency_digits', 2)), states={
                'invisible': ~Eval('different_currencies', False),
                },
            depends=['different_currencies', 'company_currency_digits']),
        'get_amount')

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        extra_excludes = ['company_total_amount_cache',
            'company_tax_amount_cache', 'company_untaxed_amount_cache']
        for exclude in extra_excludes:
            if exclude not in cls._check_modify_exclude:
                cls._check_modify_exclude.append(exclude)

    @fields.depends('company', 'currency')
    def on_change_with_different_currencies(self, name=None):
        if self.company:
            return self.company.currency != self.currency
        return False

    @fields.depends('company')
    def on_change_with_company_currency_digits(self, name=None):
        if self.company and self.company.currency:
            return self.company.currency.digits
        return 2

    @classmethod
    def get_amount(cls, invoices, names):
        pool = Pool()
        Currency = pool.get('currency.currency')

        new_names = [n for n in names if not n.startswith('company_')]
        for fname in ('untaxed_amount', 'tax_amount', 'total_amount'):
            if 'company_%s' % fname in names and fname not in new_names:
                new_names.append(fname)
        result = super(Invoice, cls).get_amount(invoices, new_names)

        company_names = [n for n in names if n.startswith('company_')]
        if company_names:
            for invoice in invoices:
                for fname in company_names:
                    if getattr(invoice, '%s_cache' % fname):
                        value = getattr(invoice, '%s_cache' % fname)
                    else:
                        with Transaction().set_context(
                                date=invoice.currency_date):
                            value = Currency.compute(invoice.currency,
                                result[fname[8:]][invoice.id],
                                invoice.company.currency, round=True)
                    result.setdefault(fname, {})[invoice.id] = value
        for key in list(result.keys()):
            if key not in names:
                del result[key]
        return result

    @classmethod
    def validate_invoice(cls, invoices):
        to_write = []
        for invoice in invoices:
            if invoice.type == 'in':
                values = cls._save_company_currency_amounts(invoice)
                to_write.extend(([invoice], values))
        if to_write:
            cls.write(*to_write)
        super(Invoice, cls).validate_invoice(invoices)

    @classmethod
    def post(cls, invoices):
        to_write = []
        for invoice in invoices:
            values = cls._save_company_currency_amounts(invoice)
            to_write.extend(([invoice], values))
        if to_write:
            cls.write(*to_write)
        super(Invoice, cls).post(invoices)

    @classmethod
    def draft(cls, invoices):
        to_write = [invoices, {
                'company_untaxed_amount_cache': None,
                'company_tax_amount_cache': None,
                'company_total_amount_cache': None,
                }]
        cls.write(*to_write)
        super(Invoice, cls).draft(invoices)

    @classmethod
    def copy(cls, invoices, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['company_untaxed_amount_cache'] = None
        default['company_tax_amount_cache'] = None
        default['company_total_amount_cache'] = None
        return super(Invoice, cls).copy(invoices, default=default)

    @classmethod
    def _save_company_currency_amounts(cls, invoice):
        pool = Pool()
        Currency = pool.get('currency.currency')
        with Transaction().set_context(date=invoice.currency_date):
            values = {}
            for fname in ('untaxed_amount', 'tax_amount', 'total_amount'):
                value = Currency.compute(invoice.currency,
                    getattr(invoice, fname), invoice.company.currency,
                    round=True)
                values['company_%s_cache' % fname] = value
        return values


class InvoiceTax(metaclass=PoolMeta):
    __name__ = 'account.invoice.tax'
    company_currency_digits = fields.Function(
        fields.Integer('Currency Digits'),
        'get_company_currency_digits')
    company_base = fields.Function(fields.Numeric('Base (Company Currency)',
            digits=(16, Eval('_parent_invoice',
                    {}).get('company_currency_digits', 2)),
            states={
                'invisible': ~Eval('_parent_invoice',
                        {}).get('different_currencies', False),
                }),
        'get_amount')
    company_amount = fields.Function(
        fields.Numeric('Amount (Company Currency)',
            digits=(16, Eval('_parent_invoice',
                    {}).get('company_currency_digits', 2)),
            states={
                'invisible': ~Eval('_parent_invoice',
                        {}).get('different_currencies', False),
                }, depends=['company_currency_digits']),
        'get_amount')

    def get_company_currency_digits(self, name):
        return self.invoice.company.currency.digits

    @classmethod
    def get_amount(cls, invoice_taxes, names):
        pool = Pool()
        Currency = pool.get('currency.currency')

        result = {}
        for invoice_tax in invoice_taxes:
            for fname in names:
                with Transaction().set_context(
                        date=invoice_tax.invoice.currency_date):
                    value = Currency.compute(invoice_tax.invoice.currency,
                        getattr(invoice_tax, fname[8:]),
                        invoice_tax.invoice.company.currency, round=True)
                result.setdefault(fname, {})[invoice_tax.id] = value
        return result


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    company_currency_digits = fields.Function(
        fields.Integer('Currency Digits'),
        'get_company_currency_digits')
    company_amount = fields.Function(
        fields.Numeric('Amount (Company Currency)',
            digits=(16, Eval('_parent_invoice', {}).get(
                    'company_currency_digits',
                    Eval('company_currency_digits', 2))),
            depends=['company_currency_digits']), 'get_company_amount')

    def get_company_currency_digits(self, name):
        return self.invoice.company.currency.digits

    def get_company_amount(self, name):
        pool = Pool()
        Date = pool.get('ir.date')
        Currency = pool.get('currency.currency')
        if self.invoice.currency == self.invoice.company.currency:
            return self.amount
        with Transaction().set_context(date=self.invoice.currency_date
                or Date.today()):
            return Currency.compute(self.invoice.currency,
                    self.amount,
                    self.invoice.company.currency, round=True)

# This file is part account_payment_gateway_invoice module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from decimal import Decimal

__all__ = ['Invoice']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'
    gateway_amount = fields.Function(fields.Numeric("Gateway Amount"),
        "get_gateway_amount")

    @classmethod
    def get_gateway_amount(cls, invoices, names):
        Transaction = Pool().get('account.payment.gateway.transaction')

        origins = ['account.invoice,%s' % invoice.id for invoice in invoices]
        transactions = Transaction.search([
            ('origin', 'in', origins),
            ('state', '=', 'done'),
            ])

        result = {n: {i.id: Decimal(0) for i in invoices} for n in names}
        for name in names:
            for invoice in invoices:
                for transaction in transactions:
                    if transaction.origin == invoice:
                        result[name][invoice.id] += transaction.amount
        return result

    @classmethod
    def workflow_to_posted(cls, invoices):
        cls.validate_invoice(invoices)
        cls.post(invoices)

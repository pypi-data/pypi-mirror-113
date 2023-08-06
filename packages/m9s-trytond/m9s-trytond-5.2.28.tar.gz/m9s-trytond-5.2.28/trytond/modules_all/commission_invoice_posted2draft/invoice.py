# This file is part of commission_invoice_posted2draft module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta


__all__ = ['Invoice']

class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def post(cls, invoices):
        Commission = Pool().get('commission')
        ids = [i.id for i in invoices
            if i.state not in ['posted', 'paid']]
        to_delete = Commission.search([
                ('origin.invoice', 'in', ids, 'account.invoice.line'),
                ])
        Commission.delete(to_delete)
        super(Invoice, cls).post(invoices)

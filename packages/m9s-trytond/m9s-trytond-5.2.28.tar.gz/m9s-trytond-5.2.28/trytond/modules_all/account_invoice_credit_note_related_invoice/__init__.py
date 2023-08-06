# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice


def register():
    Pool.register(
        invoice.Invoice,
        module='account_invoice_credit_note_related_invoice', type_='model')
    Pool.register(
        invoice.CreditInvoice,
        module='account_invoice_credit_note_related_invoice', type_='wizard')

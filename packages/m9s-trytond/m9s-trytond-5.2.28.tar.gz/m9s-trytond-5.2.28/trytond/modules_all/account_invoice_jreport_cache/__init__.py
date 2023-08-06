# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice


def register():
    Pool.register(
        invoice.Invoice,
        module='account_invoice_jreport_cache', type_='model')
    Pool.register(
        invoice.InvoiceReport,
        module='account_invoice_jreport_cache', type_='report')

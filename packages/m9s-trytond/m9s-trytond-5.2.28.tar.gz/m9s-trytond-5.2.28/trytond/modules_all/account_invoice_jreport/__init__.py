# This file is part account_invoice_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import account_invoice


def register():
    Pool.register(
        account_invoice.Invoice,
        module='account_invoice_jreport', type_='model')
    Pool.register(
        account_invoice.InvoiceReport,
        module='account_invoice_jreport', type_='report')

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice
from . import sale


def register():
    Pool.register(
        invoice.InvoiceLine,
        module='asset_invoice', type_='model')
    Pool.register(
        sale.Sale,
        sale.SaleLine,
        module='asset_invoice', type_='model', depends=['sale'])

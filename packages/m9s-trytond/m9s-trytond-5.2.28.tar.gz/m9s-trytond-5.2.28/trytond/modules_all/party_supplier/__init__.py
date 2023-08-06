# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party
from . import invoice
from . import purchase
from . import product


def register():
    Pool.register(
        party.Party,
        module='party_supplier', type_='model')
    Pool.register(
        invoice.Invoice,
        invoice.InvoiceLine,
        depends=['account_invoice'],
        module='party_supplier', type_='model')
    Pool.register(
        purchase.Purchase,
        product.ProductSupplier,
        depends=['purchase'],
        module='party_supplier', type_='model')

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party


def register():
    Pool.register(
        party.Party,
        module='party_customer', type_='model')
    Pool.register(
        party.Sale,
        depends = ['sale'],
        module='party_customer', type_='model')
    Pool.register(
        party.Invoice,
        party.InvoiceLine,
        depends=['account_invoice'],
        module='party_customer', type_='model')

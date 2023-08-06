# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import party


def register():
    Pool.register(
        party.Party,
        module='party_validate', type_='model')
    Pool.register(
        party.Invoice,
        depends=['account_invoice'],
        module='party_validate', type_='model')
    Pool.register(
        party.Sale,
        depends=['sale'],
        module='party_validate', type_='model')
    Pool.register(
        party.Purchase,
        depends=['purchase'],
        module='party_validate', type_='model')

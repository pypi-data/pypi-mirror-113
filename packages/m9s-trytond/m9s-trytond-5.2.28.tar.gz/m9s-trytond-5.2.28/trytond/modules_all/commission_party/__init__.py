# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import party
from . import invoice
from . import sale


def register():
    Pool.register(
        party.Party,
        party.Agent,
        party.PartyCommissionAgent,
        invoice.Invoice,
        module='commission_party', type_='model')
    Pool.register(
        configuration.SaleConfiguration,
        sale.Sale,
        module='commission_party', type_='model',
        depends=['sale'])
    Pool.register(
        sale.Opportunity,
        module='commission_party', type_='model',
        depends=['sale_opportunity'])

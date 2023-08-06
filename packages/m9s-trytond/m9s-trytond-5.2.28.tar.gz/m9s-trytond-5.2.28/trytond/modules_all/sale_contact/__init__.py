# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale


def register():
    Pool.register(
        sale.ConfigurationRelationType,
        sale.Configuration,
        sale.Sale,
        module='sale_contact', type_='model')

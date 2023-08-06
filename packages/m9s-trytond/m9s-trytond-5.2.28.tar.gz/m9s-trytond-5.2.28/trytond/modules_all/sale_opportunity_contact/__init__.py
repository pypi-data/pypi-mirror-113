# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .opportunity import Opportunity


def register():
    Pool.register(
        Opportunity,
        module='sale_opportunity_contact', type_='model')

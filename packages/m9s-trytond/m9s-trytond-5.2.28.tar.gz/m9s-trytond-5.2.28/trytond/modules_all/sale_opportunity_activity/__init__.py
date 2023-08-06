# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import activity


def register():
    Pool.register(
        activity.Activity,
        activity.SaleOpportunity,
        module='sale_opportunity_activity', type_='model')

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale


def register():
    Pool.register(
        sale.Sale,
        sale.RecomputePriceStart,
        module='sale_price_list_recompute_price', type_='model')
    Pool.register(
        sale.RecomputePrice,
        module='sale_price_list_recompute_price', type_='wizard')

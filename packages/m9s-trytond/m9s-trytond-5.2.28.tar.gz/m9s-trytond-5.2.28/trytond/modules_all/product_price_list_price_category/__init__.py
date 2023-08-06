# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product


def register():
    Pool.register(
        product.PriceListCategory,
        product.Template,
        product.PriceList,
        product.PriceListLine,
        module='product_price_list_price_category', type_='model')

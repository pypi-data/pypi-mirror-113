# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale

def register():
    Pool.register(
        sale.SaleLine,
        module='product_sale_line_relation', type_='model')

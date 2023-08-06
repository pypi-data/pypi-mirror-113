# This file is part product_search_code module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import product

def register():
    Pool.register(
        product.Template,
        module='product_search_code', type_='model')

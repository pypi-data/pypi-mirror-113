# This file is part stock_move module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import product

def register():
    Pool.register(
        product.ProductMoves,
        module='stock_move', type_='wizard')

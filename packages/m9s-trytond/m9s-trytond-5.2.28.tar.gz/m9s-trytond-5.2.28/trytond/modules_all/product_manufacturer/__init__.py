# This file is part product_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import move
from . import product
from . import purchase
from . import sale


def register():
    Pool.register(
        move.Move,
        product.Template,
        product.Product,
        purchase.PurchaseLine,
        sale.SaleLine,
        module='product_manufacturer', type_='model')

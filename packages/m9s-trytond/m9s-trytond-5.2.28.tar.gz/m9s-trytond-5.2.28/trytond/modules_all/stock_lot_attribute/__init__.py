# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .stock import *


def register():
    Pool.register(
        LotAttributeSet,
        LotAttribute,
        LotAttributeAttributeSet,
        Template,
        Lot,
        module='stock_lot_attribute', type_='model')

# This file is part stock_lot_by_location module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import stock

def register():
    Pool.register(
        stock.LotByLocations,
        module='stock_lot_by_location', type_='wizard')

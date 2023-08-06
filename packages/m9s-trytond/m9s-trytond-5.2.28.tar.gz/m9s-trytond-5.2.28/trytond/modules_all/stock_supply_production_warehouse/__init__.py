# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import production


def register():
    Pool.register(
        production.StockSupplyStart,
        module='stock_supply_production_warehouse', type_='model')
    Pool.register(
        production.StockSupply,
        module='stock_supply_production_warehouse', type_='wizard')

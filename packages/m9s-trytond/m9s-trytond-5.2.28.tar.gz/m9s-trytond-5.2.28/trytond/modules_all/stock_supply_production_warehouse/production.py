# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['StockSupplyStart', 'StockSupply']


class StockSupplyStart(metaclass=PoolMeta):
    __name__ = 'stock.supply.start'

    warehouses = fields.Many2Many('stock.location', None, None, 'Warehouses',
        domain=[
            ('type', '=', 'warehouse'),
            ])


class StockSupply(metaclass=PoolMeta):
    __name__ = 'stock.supply'


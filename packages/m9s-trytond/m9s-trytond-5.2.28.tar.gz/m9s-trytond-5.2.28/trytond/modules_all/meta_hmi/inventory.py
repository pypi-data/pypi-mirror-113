# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta


class Inventory(metaclass=PoolMeta):
    __name__ = 'stock.inventory'

    @staticmethod
    def default_location():
        Location = Pool().get('stock.location')
        warehouses = Location.search([
                ('code', '=', 'STO'),
                ])
        if len(warehouses) == 1:
            return warehouses[0].id

    @staticmethod
    def default_empty_quantity():
        return 'keep'

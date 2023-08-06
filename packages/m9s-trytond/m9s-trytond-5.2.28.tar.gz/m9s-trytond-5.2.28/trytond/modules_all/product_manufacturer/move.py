# This file is part product_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Move']


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'
    manufacturer = fields.Function(
        fields.Many2One('party.party', 'Manufacturer'), 'get_manufacturer')

    @classmethod
    def get_manufacturer(cls, records, name):
        result = {}
        for line in records:
            result[line.id] = line.product.manufacturer and \
                line.product.manufacturer.id or None
        return result

    def on_change_product(self):
        super(Move, self).on_change_product()

        self.manufacturer = None
        if self.product:
            self.manufacturer = self.product.manufacturer or None

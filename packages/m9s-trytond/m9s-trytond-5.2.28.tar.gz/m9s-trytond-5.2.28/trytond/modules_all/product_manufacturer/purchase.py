# This file is part product_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['PurchaseLine']


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'
    manufacturer = fields.Function(
        fields.Many2One('party.party', 'Manufacturer'),
        'get_manufacturer')

    @classmethod
    def get_manufacturer(cls, records, name):
        result = {}
        for line in records:
            result[line.id] = (line.product.manufacturer.id
                if line.product and line.product.manufacturer
                else None)
        return result

    def on_change_product(self):
        super(PurchaseLine, self).on_change_product()

        self.manufacturer = None
        if self.product:
            self.manufacturer = self.product.manufacturer or None

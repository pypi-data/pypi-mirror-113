# This file is part product_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Template', 'Product']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    manufacturer = fields.Many2One('party.party', 'Manufacturer',
        domain=[('manufacturer', '=', True)])
    manufacturer_name = fields.Char('Manufacturer Name')


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'
    manufacturer_code = fields.Char('Manufacturer Code')

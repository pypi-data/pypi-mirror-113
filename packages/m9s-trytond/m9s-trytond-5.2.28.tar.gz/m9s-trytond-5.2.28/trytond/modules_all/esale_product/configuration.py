# This file is part esale_product module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Configuration']


class Configuration(metaclass=PoolMeta):
    __name__ = 'product.configuration'
    esale_attribute_group = fields.Many2One('esale.attribute.group',
            'eSale Attribute Group')
    esale_media_uri = fields.Char('Media URI',
        help='eSale Media URI')

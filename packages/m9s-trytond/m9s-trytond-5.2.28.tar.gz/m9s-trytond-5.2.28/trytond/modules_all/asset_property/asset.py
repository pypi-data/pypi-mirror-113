# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['Asset']


class Asset(metaclass=PoolMeta):
    __name__ = 'asset'

    home_assessment = fields.Char('Home Assessment')
    energy_certificate = fields.Char('Energy Certificate')
    land_register = fields.Char('Land Register')

    @classmethod
    def __setup__(cls):
        super(Asset, cls).__setup__()
        item = ('property', 'Property')
        if item not in cls.type.selection:
            cls.type.selection.append(item)


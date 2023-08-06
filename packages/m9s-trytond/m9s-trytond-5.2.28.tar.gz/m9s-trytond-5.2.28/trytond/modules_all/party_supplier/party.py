# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.modules.party.party import STATES, DEPENDS

__all__ = ['Party']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    supplier = fields.Boolean('Supplier', states=STATES, depends=DEPENDS)

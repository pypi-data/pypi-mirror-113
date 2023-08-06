# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Party']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    manufacturer = fields.Boolean('Manufacturer',
        help="Check this box if the partner is a manufacturer.")

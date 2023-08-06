# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['SaleConfiguration']


class SaleConfiguration(metaclass=PoolMeta):
    __name__ = 'sale.configuration'
    agent_party = fields.Selection([
            ('party', 'Party'),
            ('shipment_party', 'Shipment Party'),
        ], 'Agent Party', help='Default Agent Party')

    @staticmethod
    def default_agent_party():
        return 'party'

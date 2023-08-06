# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields, ModelSQL

__all__ = ['SaleLine']

SALE_LINE_FIELD_MAP = {
    'sale_party': 'party',
    'sale_state': 'state',
    'sale_date': 'sale_date',
    'sale_shipment_party': 'shipment_party',
    }


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    sale_party = fields.Function(fields.Many2One('party.party', 'Sale Party'),
        'get_sale_field', searcher='search_sale_field')
    sale_shipment_party = fields.Function(fields.Many2One('party.party',
            'Sale Shipment Party'), 'get_sale_field',
        searcher='search_sale_field')
    sale_date = fields.Function(fields.Date('Sale Date'), 'get_sale_field',
        searcher='search_sale_field')

    def get_sale_field(self, name):
        name = SALE_LINE_FIELD_MAP[name]
        if not self.sale:
            return
        value = getattr(self.sale, name)
        if value and isinstance(value, ModelSQL):
            value = value.id
        return value

    @classmethod
    def search_sale_field(cls, name, clause):
        name = SALE_LINE_FIELD_MAP[name]
        return [('sale.' + name,) + tuple(clause[1:])]

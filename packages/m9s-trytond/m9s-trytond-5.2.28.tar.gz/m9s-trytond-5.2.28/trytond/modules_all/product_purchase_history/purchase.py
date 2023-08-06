# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import Pool, PoolMeta

__all__ = ['PurchaseLine']


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'
    number = fields.Function(fields.Char('Number'),
        'get_purchase_field', searcher='search_purchase_field')
    purchase_date = fields.Function(fields.Date('Purchase Date'),
        'get_purchase_field', searcher='search_purchase_field')
    party = fields.Function(fields.Many2One('party.party', 'Party'),
        'get_purchase_field', searcher='search_purchase_field')
    currency = fields.Function(fields.Many2One('currency.currency',
        'Currency'), 'get_purchase_field', searcher='search_purchase_field')

    @classmethod
    def __setup__(cls):
        super(PurchaseLine, cls).__setup__()
        cls._order.insert(0, ('purchase_date', 'DESC'))
        cls._order.insert(1, ('id', 'ASC'))

    def get_purchase_field(self, name):
        field = getattr(self.__class__, name)
        value = getattr(self.purchase, name)
        if isinstance(value, ModelSQL):
            if field._type == 'reference':
                return str(value)
            return value.id
        return value

    @classmethod
    def search_purchase_field(cls, name, clause):
        nested = clause[0].lstrip(name)
        return [('purchase.' + name + nested,) + tuple(clause[1:])]

    def _order_purchase_field(name):
        def order_field(tables):
            pool = Pool()
            Purchase = pool.get('purchase.purchase')
            field = Purchase._fields[name]
            table, _ = tables[None]
            purchase_tables = tables.get('purchase')
            if purchase_tables is None:
                purchase = Purchase.__table__()
                purchase_tables = {
                    None: (purchase, purchase.id == table.purchase),
                    }
                tables['purchase'] = purchase_tables
            return field.convert_order(name, purchase_tables, Purchase)
        return staticmethod(order_field)
    order_party = _order_purchase_field('party')
    order_currency = _order_purchase_field('currency')
    order_purchase_date = _order_purchase_field('purchase_date')

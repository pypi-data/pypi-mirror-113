# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['Opportunity', 'Priority']


class Priority(ModelSQL, ModelView):
    'Priority'
    __name__ = 'sale.opportunity.priority'
    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence')

    @classmethod
    def __setup__(cls):
        super(Priority, cls).__setup__()
        cls._order.insert(0, ('sequence', 'ASC'))

    @staticmethod
    def order_sequence(tables):
        table, _ = tables[None]
        return [table.sequence == None, table.sequence]


class Opportunity(metaclass=PoolMeta):
    __name__ = 'sale.opportunity'
    priority = fields.Many2One('sale.opportunity.priority', 'Priority')

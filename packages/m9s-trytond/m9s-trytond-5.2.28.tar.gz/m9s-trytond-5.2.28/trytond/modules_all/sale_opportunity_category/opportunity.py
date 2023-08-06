# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['Opportunity', 'Category']


class Category(ModelSQL, ModelView):
    'Category'
    __name__ = 'sale.opportunity.category'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code')

class Opportunity(metaclass=PoolMeta):
    __name__ = 'sale.opportunity'

    category = fields.Many2One('sale.opportunity.category',
        'Category')

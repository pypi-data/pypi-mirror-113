# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from sql import Null

from trytond.model import ModelSQL, ModelView, sequence_ordered, fields
from trytond.pool import Pool

__all__ = ['Category', 'Description']


class Category(sequence_ordered(), ModelSQL, ModelView):
    'Typfied Description Category'
    __name__ = 'typified.description.category'

    name = fields.Char('Name', translate=True, required=True)


class Description(sequence_ordered(), ModelSQL, ModelView):
    'Typified Description'
    __name__ = 'typified.description'

    name = fields.Char('Name', translate=True, required=True)
    category = fields.Many2One('typified.description.category', 'Category',
        select=True)
    description = fields.Text('Description', translate=True, required=True)
    category_sequence = fields.Function(fields.Integer('Category Sequence'),
        'get_category_sequence')

    @classmethod
    def __setup__(cls):
        super(Description, cls).__setup__()
        cls._order.insert(0, ('category_sequence', 'ASC'))

    def get_category_sequence(self, name):
        if self.category:
            return self.category.sequence

    @staticmethod
    def order_category_sequence(tables):
        pool = Pool()
        Category = pool.get('typified.description.category')
        table, _ = tables[None]
        category_table = tables.get('category')
        if category_table is None:
            category = Category.__table__()
            category_table = {
                None: (category, category.id == table.category),
                }
            tables['category'] = category_table
        table, _ = category_table[None]
        return [table.sequence == Null, table.sequence]

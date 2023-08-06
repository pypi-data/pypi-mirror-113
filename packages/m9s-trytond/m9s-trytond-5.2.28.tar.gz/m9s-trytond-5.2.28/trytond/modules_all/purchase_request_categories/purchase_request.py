# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['PurchaseRequest']


class PurchaseRequest(metaclass=PoolMeta):
    __name__ = 'purchase.request'

    categories = fields.Function(fields.Many2Many('product.category',
        None, None, 'Categories'),
        'get_categories', searcher='search_categories_field')

    def get_categories(self, name):
        res = []
        if self.product:
            res += [x.id for x in getattr(self.product, name)]
        return res

    @classmethod
    def search_categories_field(cls, name, clause):
        return [tuple(('product.' + name,)) + tuple(clause[1:])]

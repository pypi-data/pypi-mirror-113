# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['Category']


class Category(metaclass=PoolMeta):
    __name__ = "product.category"
    products = fields.Many2Many('product.template-product.category.all',
        'category', 'template', "Products", readonly=True)

    @classmethod
    def copy(cls, records, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['products'] = None
        return super(Category, cls).copy(records, default=default)

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import Unique
from trytond.pool import PoolMeta

__all__ = ['Product']


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    @classmethod
    def __setup__(cls):
        super(Product, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints += [
            ('code_uniq', Unique(t, t.code),
                'The Code of the Product must be unique.'),
            ]

    @classmethod
    def copy(cls, products, default=None):
        if default is None:
            default = {}
        if 'code' in default:
            return super(Product, cls).copy(products, default)
        default = default.copy()
        result = []
        for product in products:
            default['code'] = '%s (%d)' % (product.code, 2)
            result += super(Product, cls).copy([product], default)
        return result

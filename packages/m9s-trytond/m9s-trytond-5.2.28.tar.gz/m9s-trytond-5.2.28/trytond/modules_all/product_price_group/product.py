# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.pyson import Id, Eval

__all__ = ['Template', 'Product', 'ProductSupplier']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()

        # cost price
        invisible_cost_price = ~Id('product_price_group',
                'group_product_cost_price').in_(
                Eval('context', {}).get('groups', []))
        if 'invisible' in cls.cost_price.states:
            cls.cost_price.states['invisible'] &= invisible_cost_price
        else:
            cls.cost_price.states['invisible'] = invisible_cost_price

        # list price
        invisible_list_price = ~Id('product_price_group',
                'group_product_list_price').in_(
                Eval('context', {}).get('groups', []))
        if 'invisible' in cls.list_price.states:
            cls.list_price.states['invisible'] &= invisible_list_price
        else:
            cls.list_price.states['invisible'] = invisible_list_price


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    @classmethod
    def __setup__(cls):
        super(Product, cls).__setup__()

        # cost price
        invisible_cost_price = ~Id('product_price_group',
                'group_product_cost_price').in_(
                Eval('context', {}).get('groups', []))
        if 'invisible' in cls.cost_price.states:
            cls.cost_price.states['invisible'] &= invisible_cost_price
        else:
            cls.cost_price.states['invisible'] = invisible_cost_price

        # list price
        invisible_list_price = ~Id('product_price_group',
                'group_product_list_price').in_(
                Eval('context', {}).get('groups', []))
        if 'invisible' in cls.list_price.states:
            cls.list_price.states['invisible'] &= invisible_list_price
        else:
            cls.list_price.states['invisible'] = invisible_list_price


class ProductSupplier(metaclass=PoolMeta):
    __name__ = 'purchase.product_supplier'

    @classmethod
    def __setup__(cls):
        super(ProductSupplier, cls).__setup__()

        # supplier prices
        invisible_prices = ~Eval('groups', []).contains(
                Id('product_price_group', 'group_product_cost_price'))
        if 'invisible' not in cls.prices.states:
            cls.prices.states['invisible'] = invisible_prices
        else:
            cls.prices.states['invisible'] &= invisible_prices

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.modules.product.product import STATES, DEPENDS

__all__ = ['PriceListCategory', 'Template', 'PriceList', 'PriceListLine']


class PriceListCategory(ModelSQL, ModelView):
    'Price List Category'
    __name__ = 'product.price_list.category'
    name = fields.Char('Name', translate=True, required=True)

    @classmethod
    def __setup__(cls):
        super(PriceListCategory, cls).__setup__()
        cls._order = [
            ('name', 'ASC'),
            ('id', 'DESC'),
            ]


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    price_list_category = fields.Many2One('product.price_list.category',
        'Price List Category', states=STATES, depends=DEPENDS)


class PriceList(metaclass=PoolMeta):
    __name__ = 'product.price_list'

    def compute(self, party, product, unit_price, quantity, uom,
            pattern=None):
        'Add the product\'s price list category in pattern.'
        if pattern is None:
            pattern = {}

        pattern = pattern.copy()
        if product:
            pattern['price_list_category'] = (product.price_list_category and
                product.price_list_category.id or None)
        return super(PriceList, self).compute(party, product, unit_price,
            quantity, uom, pattern)


class PriceListLine(metaclass=PoolMeta):
    __name__ = 'product.price_list.line'
    price_list_category = fields.Many2One('product.price_list.category',
        'Price List Category')

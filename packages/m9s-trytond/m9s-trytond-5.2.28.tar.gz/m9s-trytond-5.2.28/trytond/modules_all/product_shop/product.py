# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import PoolMeta


__all__ = ['Template', 'TemplateSaleShop']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    shops = fields.Many2Many('product.template-sale.shop',
            'template', 'shop', 'Shops',
            help='Shops where this product will be available.')


class TemplateSaleShop(ModelSQL):
    'Product - Shop'
    __name__ = 'product.template-sale.shop'
    _table = 'product_template_sale_shop'
    template = fields.Many2One('product.template', 'Template',
        ondelete='CASCADE', select=True, required=True)
    shop = fields.Many2One('sale.shop', 'Shop', ondelete='RESTRICT',
        select=True, required=True)

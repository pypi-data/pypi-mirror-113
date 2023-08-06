# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta

from trytond.modules.product.product import STATES, DEPENDS

__all__ = ['Brand', 'Model', 'Template']


class Brand(ModelSQL, ModelView):
    '''Brand'''
    __name__ = 'product.brand'
    name = fields.Char('Name', required=True, translate=True)
    active = fields.Boolean('Active')
    description = fields.Text('Description', translate=True)
    products = fields.One2Many('product.template', 'brand', 'Products')

    @staticmethod
    def default_active():
        return True


class Model(ModelSQL, ModelView):
    '''Model'''
    __name__ = 'product.brand.model'
    name = fields.Char('Name', required=True)
    brand = fields.Many2One('product.brand', 'Brand', required=True)


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    brand = fields.Many2One('product.brand', 'Brand', states=STATES,
        depends=DEPENDS)

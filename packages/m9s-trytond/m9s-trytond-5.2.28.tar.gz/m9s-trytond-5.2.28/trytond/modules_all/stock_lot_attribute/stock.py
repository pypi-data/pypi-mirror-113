#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, DictSchemaMixin, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['LotAttributeSet', 'LotAttribute', 'LotAttributeAttributeSet',
    'Template', 'Lot']


class LotAttributeSet(ModelSQL, ModelView):
    "Lot Attribute Set"
    __name__ = 'stock.lot.attribute.set'
    name = fields.Char('Name', required=True, translate=True)
    attributes = fields.Many2Many(
        'stock.lot.attribute-stock.lot.attribute-set',
        'attribute_set', 'attribute', 'Attributes')


class LotAttribute(DictSchemaMixin, ModelSQL, ModelView):
    "Lot Attribute"
    __name__ = 'stock.lot.attribute'
    sets = fields.Many2Many('stock.lot.attribute-stock.lot.attribute-set',
        'attribute', 'attribute_set', 'Sets')


class LotAttributeAttributeSet(ModelSQL):
    "Lot Attribute - Set"
    __name__ = 'stock.lot.attribute-stock.lot.attribute-set'
    attribute = fields.Many2One('stock.lot.attribute', 'Attribute',
        ondelete='CASCADE', select=True, required=True)
    attribute_set = fields.Many2One('stock.lot.attribute.set', 'Set',
        ondelete='CASCADE', select=True, required=True)


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    lot_attribute_set = fields.Many2One('stock.lot.attribute.set', 'Lot Set')


class Lot(metaclass=PoolMeta):
    __name__ = 'stock.lot'

    attributes = fields.Dict('stock.lot.attribute', 'Attributes',
        domain=[
            ('sets', '=', Eval('attribute_set', -1)),
            ],
        states={
            'readonly': ~Eval('attribute_set')
            },
        depends=['attribute_set'])
    attribute_set = fields.Function(fields.Many2One('stock.lot.attribute.set',
            'Set'), 'on_change_with_attribute_set')

    @fields.depends('product')
    def on_change_with_attribute_set(self, name=None):
        if (self.product and
                getattr(self.product.template, 'lot_attribute_set', None)):
            return self.product.template.lot_attribute_set.id

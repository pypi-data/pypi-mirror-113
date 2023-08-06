# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.pool import PoolMeta
from trytond.modules.product.product import STATES, DEPENDS

__all__ = ['Group', 'GroupTemplate', 'Template']


class Group(ModelSQL, ModelView):
    'Group'
    __name__ = 'product.group'
    name = fields.Char('Name', required=True)


class GroupTemplate(ModelSQL):
    'Group - Template'
    __name__ = 'product.group-product.template'
    group = fields.Many2One('product.group', 'Group', required=True,
        select=True, ondelete='CASCADE')
    template = fields.Many2One('product.template', 'Template', required=True,
        select=True, ondelete='CASCADE')


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    groups = fields.Many2Many('product.group-product.template', 'template',
        'group', 'Groups', states=STATES, depends=DEPENDS)

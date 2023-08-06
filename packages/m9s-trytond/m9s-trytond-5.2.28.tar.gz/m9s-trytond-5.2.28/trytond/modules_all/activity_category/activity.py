# This file is part activity_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from sql.conditionals import Coalesce
from sql.operators import Equal

from trytond.model import (
    ModelView, ModelSQL, DeactivableMixin, fields, Exclude, tree)
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Category', 'Activity', 'ActivityCategory']

STATES = {
    'readonly': ~Eval('active'),
}
DEPENDS = ['active']


class Category(DeactivableMixin, tree(separator=' / '), ModelSQL, ModelView):
    "Category"
    __name__ = 'activity.category'
    name = fields.Char('Name', required=True, states=STATES, translate=True,
        depends=DEPENDS,
        help="The main identifier of the category.")
    parent = fields.Many2One('activity.category', 'Parent',
        select=True, states=STATES, depends=DEPENDS,
        help="Add the category below the parent.")
    childs = fields.One2Many('activity.category', 'parent',
       'Children', states=STATES, depends=DEPENDS,
        help="Add children below the category.")

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('name_parent_exclude',
                Exclude(t, (t.name, Equal), (Coalesce(t.parent, -1), Equal)),
                'activity_category.msg_category_name_unique'),
            ]
        cls._order.insert(0, ('name', 'ASC'))


class Activity(metaclass=PoolMeta):
    __name__ = 'activity.activity'
    categories = fields.Many2Many('activity.activity-activity.category',
        'activity', 'category', 'Categories',
        help="The categories the activity belongs to.")


class ActivityCategory(ModelSQL):
    'Activity - Category'
    __name__ = 'activity.activity-activity.category'
    _table = 'activity_category_rel'
    activity = fields.Many2One('activity.activity', 'Activity', ondelete='CASCADE',
            required=True, select=True)
    category = fields.Many2One('activity.category', 'Category',
        ondelete='CASCADE', required=True, select=True)

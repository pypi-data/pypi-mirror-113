# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Work']


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    priority = fields.Selection([
            ('1', 'Very Low'),
            ('2', 'Low'),
            ('3', 'Normal'),
            ('4', 'High'),
            ('5', 'Very High'),
            ], 'Priority', select=True, sort=True)

    @staticmethod
    def default_priority():
        return '3'

    @classmethod
    def order_priority(cls, tables):
        table, _ = tables[None]
        return [table.priority]

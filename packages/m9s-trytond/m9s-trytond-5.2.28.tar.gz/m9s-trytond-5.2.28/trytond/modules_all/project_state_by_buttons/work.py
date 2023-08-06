# This file is part of the project_state_by_button module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from datetime import datetime

from trytond.model import ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

__all__ = ['Work']


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    active = fields.Function(fields.Boolean('Active'), 'get_active',
        searcher='search_active')
    closing_date = fields.DateTime('Closing Date', readonly=True)

    @classmethod
    def __setup__(cls):
        super(Work, cls).__setup__()
        cls.state.readonly = True
        cls._buttons.update({
                'open': {
                    'invisible': Eval('state') != 'done',
                    'icon': 'tryton-back',
                    },
                'done': {
                    'invisible': Eval('state') != 'opened',
                    'icon': 'tryton-forward',
                    },
                })

    @classmethod
    @ModelView.button
    def open(cls, works):
        cls.write(works, {'state': 'opened'})

    @classmethod
    @ModelView.button
    def done(cls, works):
        cls.write(works, {
                'state': 'done',
                'closing_date': datetime.now().replace(microsecond=0)
                })

    @classmethod
    def get_total(cls, works, names):
        with Transaction().set_context(active_test=False):
            return super().get_total(works, names)

    def get_active(self, name):
        if self.type == 'project':
            return self.state == 'opened'
        return True

    @classmethod
    def search_active(cls, name, clause):
        pos = ['OR', [
            ('type', '=', 'task')
            ], [
            ('type', '=', 'project'),
            ('state', '=', 'opened'),
            ]
        ]
        neg = ['OR', [
                ('type', '=', 'task')
                ],[
                ('type', '=', 'project'),
                ('state', '=', 'done'),
                ]
            ]

        operator = clause[1]
        operand = clause[2]
        res = []
        if operator == 'in':
            if True in operand and False in operand:
                res = ['OR', pos, neg]
            elif True in operand:
                res = pos
            elif False in operand:
                res = neg
        elif operator in ('=', '!='):
            operator = operator == '=' and 1 or -1
            operand = operand and 1 or -1
            sign = operator * operand

            if sign > 0:
                res = pos
            else:
                res = neg
        if not res:
            res = pos
        return res

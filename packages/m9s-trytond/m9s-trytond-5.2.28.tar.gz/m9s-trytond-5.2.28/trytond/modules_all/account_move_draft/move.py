# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView
from trytond.pyson import Eval
from trytond.pool import PoolMeta

__all__ = ['Move']


class Move(metaclass=PoolMeta):
    __name__ = 'account.move'

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()
        if not 'state' in cls._check_modify_exclude:
            cls._check_modify_exclude.append('state')
        cls._buttons.update({
            'draft': {
                'invisible': Eval('state') == 'draft',
                },
            })

    @classmethod
    @ModelView.button
    def draft(cls, moves):
        cls.write(moves, {
            'state': 'draft',
            })

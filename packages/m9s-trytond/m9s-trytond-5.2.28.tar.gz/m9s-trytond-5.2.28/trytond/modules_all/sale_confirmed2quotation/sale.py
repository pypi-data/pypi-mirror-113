# This file is part of sale_confirmed2quotation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import Workflow, ModelView
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls._transitions.add(
            ('confirmed', 'quotation'),
            )
        cls._buttons.update({
                'to_quote': {
                    'invisible': Eval('state') != 'confirmed',
                    },
                })

    @classmethod
    @ModelView.button
    @Workflow.transition('quotation')
    def to_quote(cls, sales):
        pass

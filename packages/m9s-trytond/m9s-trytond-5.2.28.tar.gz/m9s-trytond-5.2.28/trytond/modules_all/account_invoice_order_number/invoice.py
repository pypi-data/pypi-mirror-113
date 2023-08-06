# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Invoice', 'Party']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    number_order = fields.Char('Order Number', states={
            'readonly': Eval('state') != 'draft',
            'required': (Eval('state').in_(['posted', 'paid']) &
                Eval('requires_order_number')),
            },
        depends=['state', 'requires_order_number'])
    requires_order_number = fields.Function(fields.Boolean(
            'Requires Order Number'),
        'on_change_with_requires_order_number',
        searcher='search_requires_order_number')

    @fields.depends('party')
    def on_change_with_requires_order_number(self, name=None):
        if self.party:
            return self.party.requires_order_number

    @classmethod
    def search_requires_order_number(cls, name, clause):
        return [('party.requires_order_number',) + tuple(clause[1:])]

    def _credit(self):
        credit = super(Invoice, self)._credit()
        credit.number_order = self.number_order
        return credit


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    requires_order_number = fields.Boolean('Requires order number')

# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Bool, Eval

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    incoterm = fields.Many2One('incoterm', 'Incoterm',
        states={
            'readonly': Eval('state').in_(['processing', 'cancel', 'done']),
            },
        depends=['state'])
    incoterm_place = fields.Char('Incoterm Name Place',
        states={
            'required': (Bool(Eval('incoterm'))
                & ~Eval('state').in_(['draft', 'quotation', 'cancel'])),
            'invisible': ~Bool(Eval('incoterm')),
            'readonly': Eval('state').in_(['processing', 'cancel', 'done']),
            },
        depends=['state', 'incoterm'])

    def on_change_party(self):
        super(Sale, self).on_change_party()

        self.incoterm = None
        self.incoterm_place = None
        if self.party:
            self.incoterm = self.party.incoterm \
                if self.party.incoterm else None
            self.incoterm_place = self.party.incoterm_place \
                if self.party.incoterm_place else None

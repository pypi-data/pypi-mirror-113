# This file is part carrier_code module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, sequence_ordered
from trytond.pool import PoolMeta

__all__ = ['Carrier']


class Carrier(sequence_ordered(), metaclass=PoolMeta):
    __name__ = 'carrier'
    active = fields.Boolean('Active')
    description = fields.Char('Description')
    code = fields.Char('Code')

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        cls._order.insert(1, ('party', 'ASC'))

    @staticmethod
    def default_active():
        return True

    def get_rec_name(self, name):
        rec_name = []
        if self.code:
            rec_name.append(self.code)
        if self.description:
            rec_name.append(self.description)
        if not rec_name:
            rec_name.append(self.party.rec_name)
            rec_name.append(self.carrier_product.rec_name)
        return ' - '.join(rec_name)

    @classmethod
    def search_rec_name(cls, name, clause):
        # not call super()
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        return [bool_op,
            ('code',) + tuple(clause[1:]),
            ('description',) + tuple(clause[1:]),
            ('party.name',) + tuple(clause[1:]),
            ]

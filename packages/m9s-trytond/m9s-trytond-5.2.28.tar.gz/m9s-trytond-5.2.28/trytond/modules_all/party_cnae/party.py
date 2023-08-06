# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields, tree
from trytond.pool import PoolMeta
from trytond.transaction import Transaction

__all__ = ['Cnae', 'Party']


class Cnae(ModelSQL, ModelView, tree(separator='/')):
    '''CNAE'''
    __name__ = 'party.cnae'
    _order = 'code'

    code = fields.Char('Code', required=True)
    name = fields.Char('Name', required=True)
    parent = fields.Many2One('party.cnae', 'Parent', select=True)
    childs = fields.One2Many('party.cnae', 'parent', string='Children')
    full_name = fields.Function(fields.Char('Full Name'),
        'get_full_name')

    def get_rec_name(self, name):
        return "[%s] %s" % (self.code, self.name)

    @classmethod
    def search_rec_name(cls, name, clause):
        return ['OR',
            ('code',) + tuple(clause[1:]),
            ('name',) + tuple(clause[1:]),
            ]

    def get_full_name(self, name):
        res = self.rec_name
        parent = self.parent
        while parent:
            res = '%s / %s' % (parent.name, res)
            parent = parent.parent
        return res


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    cnae = fields.Many2One('party.cnae', 'CNAE')

    @staticmethod
    def default_cnae():
        return Transaction().context.get('cnae')

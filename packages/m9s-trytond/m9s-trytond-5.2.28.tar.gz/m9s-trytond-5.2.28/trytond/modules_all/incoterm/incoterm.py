# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields

__all__ = ['Category', 'Incoterm']


class Category(ModelSQL, ModelView):
    'Incoterm Category'
    __name__ = 'incoterm.category'
    name = fields.Char('Name', required=True, translate=True)


class Incoterm(ModelSQL, ModelView):
    'Incoterm'
    __name__ = 'incoterm'

    name = fields.Char('Name', required=True, translate=True)
    code = fields.Char('Code', required=True)
    active = fields.Boolean('Active', select=True)
    category = fields.Many2One('incoterm.category', 'Category')
    place_required = fields.Boolean('Place required',
        help="Make place required for this incoterm")

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_place_required():
        return False

    def get_rec_name(self, name):
        return '%s - %s' % (self.code, self.name)

    @classmethod
    def search_rec_name(cls, name, clause):
        return ['OR',
            ('code',) + tuple(clause[1:]),
            ('name',) + tuple(clause[1:]),
            ]

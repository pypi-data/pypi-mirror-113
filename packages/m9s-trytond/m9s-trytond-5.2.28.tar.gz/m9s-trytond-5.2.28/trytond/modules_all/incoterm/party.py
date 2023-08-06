# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond import backend
from trytond.pool import PoolMeta, Pool
from trytond.model import fields, ModelSQL
from trytond.pyson import Eval, Bool
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

__all__ = ['Party', 'PartyIncoterm']

incoterm = fields.Many2One('incoterm', 'Incoterm')
incoterm_place = fields.Char('Incoterm Name Place',
        states={
            'required': Bool(Eval('place_required')),
            'invisible': ~Bool(Eval('place_required')),
            },
        depends=['place_required'])


class Party(CompanyMultiValueMixin, metaclass=PoolMeta):
    __name__ = 'party.party'
    incoterm = fields.MultiValue(incoterm)
    incoterm_place = fields.MultiValue(incoterm_place)
    incoterms = fields.One2Many('party.party.incoterm', 'party', "Incoterms")
    place_required = fields.Function(fields.Boolean('Place Required'),
        'on_change_with_place_required')

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'incoterm', 'incoterm_place'}:
            return pool.get('party.party.incoterm')
        return super(Party, cls).multivalue_model(field)

    @fields.depends('incoterm')
    def on_change_with_place_required(self, name=None):
        if self.incoterm:
            return self.incoterm.place_required

    @fields.depends('incoterm', 'incoterm_place')
    def on_change_incoterm(self, name=None):
        self.incoterm_place = None


class PartyIncoterm(ModelSQL, CompanyValueMixin):
    "Party Payment Term"
    __name__ = 'party.party.incoterm'
    party = fields.Many2One(
        'party.party', "Party", ondelete='CASCADE', select=True)
    incoterm = incoterm
    incoterm_place = fields.Char('Incoterm Name Place')

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(PartyIncoterm, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.extend(['incoterm', 'incoterm_place'])
        value_names.extend(['incoterm', 'incoterm_place'])
        migrate_property(
            'party.party', field_names, cls, value_names,
            parent='party', fields=fields)

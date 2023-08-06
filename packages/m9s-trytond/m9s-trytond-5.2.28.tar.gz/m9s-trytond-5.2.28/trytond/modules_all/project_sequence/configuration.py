# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond import backend
from trytond.model import ModelView, ModelSQL, ModelSingleton, fields
from trytond.pool import Pool
from trytond.pyson import Eval
from trytond.tools.multivalue import migrate_property
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)
__all__ = ['Configuration', 'ConfigurationWorkSequence']


class Configuration(
        ModelSingleton, ModelSQL, ModelView, CompanyMultiValueMixin):
    'Work Configuration'
    __name__ = 'work.configuration'

    work_sequence = fields.MultiValue(fields.Many2One('ir.sequence',
            'Work Sequence', domain=[
                ('code', '=', 'project.work'),
                ('company', 'in',
                    [Eval('context', {}).get('company', -1), None]),
                ]))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'work_sequence'}:
            return pool.get('work.configuration.work_sequence')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationWorkSequence(ModelSQL, CompanyValueMixin):
    "Work Sequence Value"
    __name__ = 'work.configuration.work_sequence'

    work_sequence = fields.Many2One('ir.sequence',
            'Work Sequence', domain=[
                ('code', '=', 'project.work'),
                ('company', 'in',
                    [Eval('company', -1), None]),
                ], depends=['company'])

    @classmethod
    def __register__(cls, module_name):
        TableHandler = backend.get('TableHandler')
        exist = TableHandler.table_exist(cls._table)

        super(ConfigurationWorkSequence, cls).__register__(module_name)

        if not exist:
            cls._migrate_property([], [], [])

    @classmethod
    def _migrate_property(cls, field_names, value_names, fields):
        field_names.append('work_sequence')
        value_names.append('work_sequence')
        fields.append('company')
        migrate_property(
            'work.configuration', field_names, cls, value_names,
            fields=fields)

    @classmethod
    def default_work_sequence(cls):
        pool = Pool()
        Sequence = pool.get('ir.sequence')
        sequence = Sequence.search([('code', '=', 'project.work')])
        if sequence:
            return sequence[0]
        return None

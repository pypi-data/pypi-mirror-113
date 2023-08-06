# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Party']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    camerdata = fields.Boolean('Camerdata')
    imports = fields.Selection([
            (None, ''),
            ('yes', 'Yes'),
            ('no', 'No'),
            ], 'Imports?')
    exports = fields.Selection([
            (None, ''),
            ('yes', 'Yes'),
            ('no', 'No'),
            ], 'Exports?')
    employee_segment = fields.Selection([
            (None, ''),
            ('1', 'From 1 to 5 (Microcompany)'),
            ('2', 'From 6 to 10 (Microcompany)'),
            ('3', 'From 11 to 25 (Small company)'),
            ('4', 'From 26 to 50 (Small company)'),
            ('5', 'From 51 to 100 (Medium company)'),
            ('6', 'From 101 to 250 (Medium company)'),
            ('7', 'From 251 to 500 (Big company)'),
            ('8', 'More than 500 (Big company)'),
            ], 'Employees')
    turnover = fields.Selection([
            (None, ''),
            ('1', 'Until 300.000'),
            ('2', 'From 300.001 to 600.000'),
            ('3', 'From 600.001 to 1.500.000'),
            ('4', 'From 1.500.001 to 3.000.000'),
            ('5', 'From 3.000.001 to 6.000.000'),
            ('6', 'From 6.000.001 to 15.000.000'),
            ('7', 'From 15.000.001 to 30.000.000'),
            ('8', 'From 30.000.001 to 60.000.000'),
            ('9', 'More than 60.000.000'),
            ], 'Bussines Size')
    foundation_year = fields.Integer('Foundation Year')
    positions = fields.Text('Positions')
    legal_form = fields.Selection([
            (None, ''),
            ('01', 'Public Limited Company (PLC)'),
            ('02', 'Limited Liability Company (LLC)'),
            # (, 'Sociedad Colectiva'),
            # (, 'Sociedad Comanditaria'),
            # (, 'Comunidad de Bienes'),
            ('06', 'Cooperative'),
            ('07', 'Association'),
            ('08', 'Local Corporation'),
            ('09', 'Public Agency'),
            # (, 'Organismos de la Administracion'),
            # (, 'Comunidad de Propietarios'),
            # (, 'Sociedad Civil'),
            ('14', 'Temporary Consortium (spanish UTE)'),
            ('15', 'Other not defined types'),
            ('16', 'Congregation and Religious Institution'),
            # (, 'Entidad Extranjera'),
            ('18', 'Non-resident entity in Spain'),
            ], 'Legal Form')
    offices = fields.Integer('Offices')

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from simpleeval import simple_eval
from trytond.model import fields, Unique
from trytond.pool import PoolMeta
from trytond.pyson import Bool, Eval


__all__ = ['Template', 'QuantitativeTemplateLine', 'Test',
    'QuantitativeTestLine']


class Template(metaclass=PoolMeta):
    __name__ = 'quality.template'

    formula = fields.Text('Formula')
    unit = fields.Many2One('product.uom', 'Unit',
        states={
            'required': Bool(Eval('formula')),
            },
        depends=['formula'])
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')

    @fields.depends('unit')
    def on_change_with_unit_digits(self, name=None):
        if not self.unit:
            return 2
        return self.unit.digits


class QuantitativeTemplateLine(metaclass=PoolMeta):
    __name__ = 'quality.quantitative.template.line'

    formula_name = fields.Char('Formula Name',
        required=True,
        help='Name must follow the following rules: \n'
        '\t* Must begin with a letter (a - z, A - B) or underscore (_)\n'
        '\t* Other characters can be letters, numbers or _ \n'
        '\t* It is Case Sensitive and can be any (reasonable) length \n'
        '\t* There are some reserved words which you cannot use as a '
        'variable name because Python uses them for other other things')

    @classmethod
    def __setup__(cls):
        super(QuantitativeTemplateLine, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('template_line_name_uniq', Unique(t, t.template, t.formula_name),
                'Formula Name of Line can be used only once on Template.'),
            ]


class Test(metaclass=PoolMeta):
    __name__ = 'quality.test'
    __metaclass__ = PoolMeta

    formula = fields.Text('Formula', readonly=True)
    unit = fields.Many2One('product.uom', 'Unit',
        states={
            'required': Bool(Eval('formula')),
            },
        depends=['formula'])
    unit_digits = fields.Function(fields.Integer('Unit Digits'),
        'on_change_with_unit_digits')
    formula_result = fields.Function(fields.Float('Formula Result',
            digits=(16, Eval('unit_digits', 2)), depends=['unit_digits']),
        'get_formula_result')

    @fields.depends('unit')
    def on_change_with_unit_digits(self, name=None):
        if not self.unit:
            return 2
        return self.unit.digits

    def get_formula_result(self, name=None):
        if not self.formula:
            return
        vals = {}
        for line in self.quantitative_lines:
            if line.formula_name:
                vals[line.formula_name] = line.value or 0
        try:
            value = simple_eval(self.formula, names=vals, functions={
                    'round': round,
                    'int': int,
                    })
            return value
        except (NameError, ZeroDivisionError):
            pass

    def apply_template_values(self):
        super(Test, self).apply_template_values()
        for template in self.templates:
            if template.formula:
                self.formula = template.formula
                self.unit = template.unit
                break

    @classmethod
    def apply_templates(cls, tests):
        super(Test, cls).apply_templates(tests)
        for test in tests:
            for template in test.templates:
                test.formula = template.formula
                test.unit = template.unit

        cls.save(tests)


class QuantitativeTestLine(metaclass=PoolMeta):
    __name__ = 'quality.quantitative.test.line'

    formula_name = fields.Char('Formula Name')

    @classmethod
    def __setup__(cls):
        super(QuantitativeTestLine, cls).__setup__()
        t = cls.__table__()
        cls._sql_constraints = [
            ('test_line_name_uniq', Unique(t, t.test, t.formula_name),
                'Formula Name of Line can be used only once on Template.'),
            ]

    def set_template_line_vals(self, template_line):
        super(QuantitativeTestLine, self).set_template_line_vals(template_line)
        self.formula_name = template_line.formula_name

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, ModelView, fields, ModelSingleton

__all__ = ['Configuration']


class Configuration(ModelSingleton, ModelSQL, ModelView):
    'Shine Configuration'
    __name__ = 'shine.configuration'

    default_timeout = fields.Integer('Timeout (s)', help='Default value for '
        'timeout field in new sheets.')

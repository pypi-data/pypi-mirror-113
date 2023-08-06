# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import work
from . import configuration


def register():
    Pool.register(
        work.Work,
        configuration.Configuration,
        configuration.ConfigurationWorkSequence,
        module='project_sequence', type_='model')

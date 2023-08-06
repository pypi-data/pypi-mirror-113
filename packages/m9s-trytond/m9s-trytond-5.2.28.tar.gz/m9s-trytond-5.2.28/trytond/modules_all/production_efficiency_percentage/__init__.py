#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.pool import Pool
from . import production


def register():
    Pool.register(
        production.BOM,
        production.BOMInput,
        production.BOMOutput,
        module='production_efficiency_percentage', type_='model')

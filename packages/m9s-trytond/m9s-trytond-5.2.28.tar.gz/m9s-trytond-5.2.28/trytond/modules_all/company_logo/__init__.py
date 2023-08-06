# This file is part company_logo module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import company


def register():
    Pool.register(
        company.Company,
        module='company_logo', type_='model')

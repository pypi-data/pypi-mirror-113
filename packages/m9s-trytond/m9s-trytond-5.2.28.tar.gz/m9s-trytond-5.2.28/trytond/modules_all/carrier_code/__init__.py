# This file is part carrier_code module for Tryton.  The COPYRIGHT file at the
# top level of this repository contains the full copyright notices and license
# terms.
from trytond.pool import Pool
from . import carrier


def register():
    Pool.register(
        carrier.Carrier,
        module='carrier_code', type_='model')

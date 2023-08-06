# This file is part party_maps module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import address

def register():
    Pool.register(
        configuration.Configuration,
        address.Address,
        module='party_maps', type_='model')

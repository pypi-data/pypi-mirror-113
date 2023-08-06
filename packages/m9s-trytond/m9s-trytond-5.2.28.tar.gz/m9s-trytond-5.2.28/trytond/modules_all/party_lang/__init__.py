# This file is part party_lang module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import address


def register():
    Pool.register(
        address.Address,
        module='party_lang', type_='model')

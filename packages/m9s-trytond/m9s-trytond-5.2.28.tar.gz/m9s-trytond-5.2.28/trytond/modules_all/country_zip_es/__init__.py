# -*- encoding: utf-8 -*-
# This file is part country_zip_es module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import country_zip
from . import address


def register():
    Pool.register(
        address.Address,
        country_zip.LoadCountryZipsStart,
        module='country_zip_es', type_='model')
    Pool.register(
        country_zip.LoadCountryZips,
        module='country_zip_es', type_='wizard')

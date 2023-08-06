# This file is part bank_es module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.country_zip_es.tests.test_country_zip_es import suite
except ImportError:
    from .test_country_zip_es import suite

__all__ = ['suite']

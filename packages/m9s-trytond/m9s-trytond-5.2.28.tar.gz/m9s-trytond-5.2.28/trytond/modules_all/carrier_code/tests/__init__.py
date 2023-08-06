# This file is part carrier_code module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.carrier_code.tests.test_carrier_code import suite
except ImportError:
    from .test_carrier_code import suite

__all__ = ['suite']

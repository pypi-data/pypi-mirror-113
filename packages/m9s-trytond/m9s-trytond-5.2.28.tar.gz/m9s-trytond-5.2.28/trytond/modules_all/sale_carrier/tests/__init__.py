# This file is part sale_carrier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.sale_carrier.tests.test_sale_carrier import suite
except ImportError:
    from .test_sale_carrier import suite

__all__ = ['suite']

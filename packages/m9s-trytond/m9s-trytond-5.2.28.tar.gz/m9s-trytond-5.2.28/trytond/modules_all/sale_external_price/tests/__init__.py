# This file is part sale_external_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.sale_external_price.tests.test_sale_external_price import suite
except ImportError:
    from .test_sale_external_price import suite

__all__ = ['suite']

# This file is part sale_shop module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.sale_shop.tests.test_sale_shop import suite
except ImportError:
    from .test_sale_shop import suite

__all__ = ['suite']

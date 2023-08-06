# This file is part stock_buttons module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.stock_buttons.tests.test_stock_buttons import suite
except ImportError:
    from .test_stock_buttons import suite

__all__ = ['suite']

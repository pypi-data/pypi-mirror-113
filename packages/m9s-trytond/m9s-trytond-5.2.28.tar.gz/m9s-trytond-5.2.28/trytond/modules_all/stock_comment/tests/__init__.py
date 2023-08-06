# This file is part stock_comment module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.stock_comment.tests.test_stock_comment import suite
except ImportError:
    from .test_stock_comment import suite

__all__ = ['suite']

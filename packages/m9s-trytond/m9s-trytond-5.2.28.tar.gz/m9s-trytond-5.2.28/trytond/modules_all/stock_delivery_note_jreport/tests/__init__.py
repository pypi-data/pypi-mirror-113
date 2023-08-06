# This file is part stock_delivery_note_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.stock_delivery_note_jreport.tests.test_stock_delivery_note_jreport import suite
except ImportError:
    from .test_stock_delivery_note_jreport import suite

__all__ = ['suite']

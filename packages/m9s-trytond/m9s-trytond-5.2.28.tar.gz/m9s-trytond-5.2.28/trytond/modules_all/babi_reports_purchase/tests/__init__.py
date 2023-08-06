# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.babi_reports_purchase.tests.test_babi_reports_purchase import suite
except ImportError:
    from .test_babi_reports_purchase import suite

__all__ = ['suite']

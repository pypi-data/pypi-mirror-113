# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.account_invoice_jreport_cache.tests.test_jasper_report_invoice_cache import suite
except ImportError:
    from .test_jasper_report_invoice_cache import suite

__all__ = ['suite']

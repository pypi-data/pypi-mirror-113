# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.hide_core_reports.tests.test_hide_core_reports import suite
except ImportError:
    from .test_hide_core_reports import suite

__all__ = ['suite']

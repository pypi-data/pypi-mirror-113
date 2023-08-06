# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.babi_reports_sale_opportunity.tests.test_babi_reports_sale_opportunity import suite
except ImportError:
    from .test_babi_reports_sale_opportunity import suite

__all__ = ['suite']

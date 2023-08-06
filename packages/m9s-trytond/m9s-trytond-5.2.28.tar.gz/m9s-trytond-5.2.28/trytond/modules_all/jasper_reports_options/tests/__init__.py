# This file is part jasper_reports_options module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.jasper_reports_options.tests.test_jasper_reports_options import suite
except ImportError:
    from .test_jasper_reports_options import suite

__all__ = ['suite']

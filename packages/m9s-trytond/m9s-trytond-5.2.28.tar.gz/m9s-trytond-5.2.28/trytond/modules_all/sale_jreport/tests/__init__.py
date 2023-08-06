# This file is part sale_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.sale_jreport.tests.test_sale_jreport import suite
except ImportError:
    from .test_sale_jreport import suite

__all__ = ['suite']

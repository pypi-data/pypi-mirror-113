# This file is part purchase_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.purchase_jreport.tests.test_purchase_jreport import suite
except ImportError:
    from .test_purchase_jreport import suite

__all__ = ['suite']

# This file is part account_invoice_total module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.account_invoice_total.tests.test_account_invoice_total import suite
except ImportError:
    from .test_account_invoice_total import suite

__all__ = ['suite']

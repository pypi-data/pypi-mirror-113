# This file is part of the account_invoice_visible_payments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.account_invoice_visible_payments.tests.test_account_invoice_visible_payments import suite
except ImportError:
    from .test_account_invoice_visible_payments import suite

__all__ = ['suite']

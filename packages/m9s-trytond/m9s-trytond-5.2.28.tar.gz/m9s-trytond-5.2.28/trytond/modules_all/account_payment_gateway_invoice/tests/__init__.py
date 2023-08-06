# This file is part account_payment_gateway_invoice module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.account_payment_gateway_invoice.tests.test_account_payment_gateway_invoice import suite
except ImportError:
    from .test_account_payment_gateway_invoice import suite

__all__ = ['suite']

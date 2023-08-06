# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.account_payment_wizard.tests.test_account_payment_wizard import suite
except ImportError:
    from .test_account_payment_wizard import suite

__all__ = ['suite']

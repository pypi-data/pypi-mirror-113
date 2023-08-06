# This file is part of account_reconcile_different_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.account_reconcile_different_party.tests.test_account_reconcile_different_party import suite
except ImportError:
    from .test_account_reconcile_different_party import suite

__all__ = ['suite']

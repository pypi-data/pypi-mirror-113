# This file is part of the account_reconcile_different_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountReconcileDifferentPartyTestCase(ModuleTestCase):
    'Test Account Reconcile Different Party module'
    module = 'account_reconcile_different_party'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountReconcileDifferentPartyTestCase))
    return suite

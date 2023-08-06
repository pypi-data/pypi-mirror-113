# This file is part account_move_draft module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountMoveDraftTestCase(ModuleTestCase):
    'Test Account Move Draft module'
    module = 'account_move_draft'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountMoveDraftTestCase))
    return suite

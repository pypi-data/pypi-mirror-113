# This file is part of the account_move_line_related module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountMoveLineRelatedTestCase(ModuleTestCase):
    'Test Account Move Line Related module'
    module = 'account_move_line_related'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountMoveLineRelatedTestCase))
    return suite

# This file is part analytic_bank_statement_rule module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class AccountBankStatementAnalyticRuleTestCase(ModuleTestCase):
    'Test Account Bank Statement Analytic Rule module'
    module = 'analytic_bank_statement_rule'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountBankStatementAnalyticRuleTestCase))
    return suite

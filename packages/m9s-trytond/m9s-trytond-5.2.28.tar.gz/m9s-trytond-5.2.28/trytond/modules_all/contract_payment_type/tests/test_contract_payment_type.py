# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import doctest
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_teardown, doctest_checker


class TestContractPaymentTypeCase(ModuleTestCase):
    'Test Contract Payment Type module'
    module = 'contract_payment_type'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            TestContractPaymentTypeCase))
    suite.addTests(doctest.DocFileSuite('scenario_contract_payment_type.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite

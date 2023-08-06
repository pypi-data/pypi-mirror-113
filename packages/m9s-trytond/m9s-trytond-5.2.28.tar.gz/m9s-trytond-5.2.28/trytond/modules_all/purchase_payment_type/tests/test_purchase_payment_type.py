# This file is part of the purchase_payment_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_teardown, doctest_checker


class PurchasePaymentTypeTestCase(ModuleTestCase):
    'Test Purchase Payment Type module'
    module = 'purchase_payment_type'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PurchasePaymentTypeTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_purchase_payment_type.rst',
            tearDown=doctest_teardown, encoding='UTF-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    suite.addTests(doctest.DocFileSuite('scenario_purchase_request.rst',
            tearDown=doctest_teardown, encoding='UTF-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite

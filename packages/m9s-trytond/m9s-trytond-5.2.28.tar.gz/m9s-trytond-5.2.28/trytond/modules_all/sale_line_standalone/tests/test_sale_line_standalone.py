# This file is part of the sale_line_standalone module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_teardown, doctest_checker


class SaleLineStandaloneTestCase(ModuleTestCase):
    'Test Sale Line Standalone module'
    module = 'sale_line_standalone'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleLineStandaloneTestCase))
    suite.addTests(doctest.DocFileSuite('scenario_sale_line_standalone.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE,
            checker=doctest_checker))
    return suite

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import doctest_setup, doctest_teardown


class TestCase(ModuleTestCase):
    '''
    Test module.
    '''
    module = 'farm_prescription'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    suite.addTests(doctest.DocFileSuite('scenario_prescription_farm.rst',
        setUp=doctest_setup, tearDown=doctest_teardown, encoding='utf-8',
        optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite

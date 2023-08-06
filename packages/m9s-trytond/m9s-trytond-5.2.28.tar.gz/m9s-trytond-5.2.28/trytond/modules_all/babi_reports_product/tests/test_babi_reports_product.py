# This file is part of the babi_reports_product module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class BabiReportsProductTestCase(ModuleTestCase):
    'Test Babi Reports Product module'
    module = 'babi_reports_product'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        BabiReportsProductTestCase))
    return suite

# This file is part of the babi_reports_account module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class BabiReportsAccountTestCase(ModuleTestCase):
    'Test Babi Reports Account module'
    module = 'babi_reports_account'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        BabiReportsAccountTestCase))
    return suite

# This file is part of the purchase_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class PurchaseJreportTestCase(ModuleTestCase):
    'Test Purchase Jreport module'
    module = 'purchase_jreport'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PurchaseJreportTestCase))
    return suite

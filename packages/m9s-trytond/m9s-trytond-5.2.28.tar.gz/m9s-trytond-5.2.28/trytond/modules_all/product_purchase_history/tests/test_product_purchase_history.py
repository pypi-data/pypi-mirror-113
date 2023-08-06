#!/usr/bin/env python
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductPurchaseHistoryTestCase(ModuleTestCase):
    'Test Product Purchase Hisotry module'
    module = 'product_purchase_history'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductPurchaseHistoryTestCase))
    return suite

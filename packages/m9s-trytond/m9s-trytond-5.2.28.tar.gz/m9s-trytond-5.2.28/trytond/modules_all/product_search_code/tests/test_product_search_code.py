# This file is part of the product_search_code module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductSearchCodeTestCase(ModuleTestCase):
    'Test Product Search Code module'
    module = 'product_search_code'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductSearchCodeTestCase))
    return suite
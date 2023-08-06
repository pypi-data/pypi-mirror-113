# This file is part product_price_group module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class ProductPriceGroupTestCase(ModuleTestCase):
    'Test Product Price Group module'
    module = 'product_price_group'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProductPriceGroupTestCase))
    return suite

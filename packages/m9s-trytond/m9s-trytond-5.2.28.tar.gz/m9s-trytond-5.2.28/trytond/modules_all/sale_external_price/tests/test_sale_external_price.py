# This file is part of the sale_external_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SaleExternalPriceTestCase(ModuleTestCase):
    'Test Sale External Price module'
    module = 'sale_external_price'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SaleExternalPriceTestCase))
    return suite

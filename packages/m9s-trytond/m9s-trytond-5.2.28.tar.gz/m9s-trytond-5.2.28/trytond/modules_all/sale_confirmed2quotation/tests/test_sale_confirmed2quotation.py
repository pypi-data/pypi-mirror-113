# This file is part of the sale_confirmed2quotation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SaleConfirmed2quotationTestCase(ModuleTestCase):
    'Test Sale Confirmed2quotation module'
    module = 'sale_confirmed2quotation'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SaleConfirmed2quotationTestCase))
    return suite

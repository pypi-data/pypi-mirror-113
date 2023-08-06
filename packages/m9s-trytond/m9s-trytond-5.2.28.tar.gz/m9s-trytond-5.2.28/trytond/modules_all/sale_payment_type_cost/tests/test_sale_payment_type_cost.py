# This file is part of the sale_payment_type_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SalePaymentTypeCostTestCase(ModuleTestCase):
    'Test Sale Payment Type Cost module'
    module = 'sale_payment_type_cost'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        SalePaymentTypeCostTestCase))
    return suite
# This file is part purchase_product_supplier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class PurchaseProductSupplierTestCase(ModuleTestCase):
    'Test Purchase Product Supplier module'
    module = 'purchase_product_supplier'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PurchaseProductSupplierTestCase))
    return suite

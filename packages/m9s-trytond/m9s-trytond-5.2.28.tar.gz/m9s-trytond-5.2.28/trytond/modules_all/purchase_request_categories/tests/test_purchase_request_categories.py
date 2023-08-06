# This file is part purchase_request_categories module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class PurchaseRequestCategoriesTestCase(ModuleTestCase):
    'Test Purchase Request Categories module'
    module = 'purchase_request_categories'

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PurchaseRequestCategoriesTestCase))
    return suite

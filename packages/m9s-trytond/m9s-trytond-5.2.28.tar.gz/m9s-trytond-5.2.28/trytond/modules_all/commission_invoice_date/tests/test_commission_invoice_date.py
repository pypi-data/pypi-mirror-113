# This file is part commission_invoice_date module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class CommissionInvoiceDateTestCase(ModuleTestCase):
    'Test Commission Invoice Date module'
    module = 'commission_invoice_date'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            CommissionInvoiceDateTestCase))
    return suite

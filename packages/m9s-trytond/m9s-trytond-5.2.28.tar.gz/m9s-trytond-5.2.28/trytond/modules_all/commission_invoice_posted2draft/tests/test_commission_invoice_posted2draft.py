# This file is part of commission_invoice_posted2draft module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite
import unittest


class CommissionInvoicePosted2DraftTestCase(ModuleTestCase):
    'Test Commission Invoice Posted2Draft module'
    module = 'commission_invoice_posted2draft'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            CommissionInvoicePosted2DraftTestCase))
    return suite

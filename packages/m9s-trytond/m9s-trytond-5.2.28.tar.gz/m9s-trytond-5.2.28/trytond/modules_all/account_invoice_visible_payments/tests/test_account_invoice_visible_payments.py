# This file is part of the account_invoice_visible_payments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoiceVisiblePaymentsTestCase(ModuleTestCase):
    'Test Account Invoice Visible Payments module'
    module = 'account_invoice_visible_payments'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceVisiblePaymentsTestCase))
    return suite

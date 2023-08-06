# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AccountInvoiceLineDescriptionTestCase(ModuleTestCase):
    'Test Account Invoice Line Description module'
    module = 'account_invoice_line_description'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        AccountInvoiceLineDescriptionTestCase))
    return suite

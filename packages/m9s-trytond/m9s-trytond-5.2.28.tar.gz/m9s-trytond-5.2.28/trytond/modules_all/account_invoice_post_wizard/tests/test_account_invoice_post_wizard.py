# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
# import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase

class AccountInvoicePostWizardTestCase(ModuleTestCase):
    'Test Party module'
    module = 'account_invoice_post_wizard'

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoicePostWizardTestCase))
    return suite

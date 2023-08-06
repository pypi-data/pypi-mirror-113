# This file is part account_invoice_validate_identifier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest

import doctest

from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite
from trytond.tests.test_tryton import doctest_teardown
from trytond.tests.test_tryton import doctest_checker


class AccountInvoiceValidateIdentifierTestCase(ModuleTestCase):
    'Test Account Invoice Validate Identifier module'
    module = 'account_invoice_validate_identifier'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoiceValidateIdentifierTestCase))
    suite.addTests(doctest.DocFileSuite(
            'scenario_account_invoice_validate_identifier.rst',
            tearDown=doctest_teardown, encoding='utf-8',
            checker=doctest_checker,
            optionflags=doctest.REPORT_ONLY_FIRST_FAILURE))
    return suite

# This file is part account_invoice_type module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class AccountInvoiceTypeTestCase(ModuleTestCase):
    'Test Account Invoice Type module'
    module = 'account_invoice_type'


    @with_transaction()
    def test_invoice_type(self):
        'Create invoice'
        pool = Pool()
        Invoice = pool.get('account.invoice')
        Line = pool.get('account.invoice.line')

        values = Invoice.default_get(Invoice._fields.keys(),
            with_rec_name=False)
        invoice = Invoice(**values)
        lvalues = Line.default_get(Line._fields.keys(), with_rec_name=False)

        line = Line(**lvalues)
        line.quantity = 1
        line.unit_price = Decimal('12.00')
        line.amount = line.on_change_with_amount()
        invoice.lines = [line]
        invoice.on_change_lines()
        self.assertEqual(invoice.on_change_with_invoice_type(), 'out_invoice')

        line = Line(**lvalues)
        line.quantity = 1
        line.unit_price = Decimal('-12.00')
        line.amount = line.on_change_with_amount()
        invoice.lines = [line]
        invoice.on_change_lines()
        self.assertEqual(invoice.on_change_with_invoice_type(), 'out_credit_note')


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountInvoiceTypeTestCase))
    return suite

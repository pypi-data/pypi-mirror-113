# This file is part of the stock_delivery_note_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class StockDeliveryNoteJreportTestCase(ModuleTestCase):
    'Test Stock Delivery Note Jreport module'
    module = 'stock_delivery_note_jreport'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockDeliveryNoteJreportTestCase))
    return suite

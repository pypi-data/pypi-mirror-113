# This file is part stock_lot_by_location module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class StockLotByLocationTestCase(ModuleTestCase):
    'Test Stock Lot By Location module'
    module = 'stock_lot_by_location'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockLotByLocationTestCase))
    return suite

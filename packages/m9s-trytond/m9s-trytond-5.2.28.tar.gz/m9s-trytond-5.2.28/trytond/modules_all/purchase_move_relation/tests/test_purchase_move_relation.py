# This file is part purchase_move_relation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class PurchaseMoveRelationTestCase(ModuleTestCase):
    'Test Purchase Move Relation module'
    module = 'purchase_move_relation'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PurchaseMoveRelationTestCase))
    return suite

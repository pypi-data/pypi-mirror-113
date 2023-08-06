# This file is part product_category_sequence module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class ProductCategorySequenceTestCase(ModuleTestCase):
    'Test Product Category Sequence module'
    module = 'product_category_sequence'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ProductCategorySequenceTestCase))
    return suite

# This file is part activity_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest


from trytond.tests.test_tryton import ModuleTestCase
from trytond.tests.test_tryton import suite as test_suite


class ActivityCategoryTestCase(ModuleTestCase):
    'Test Activity Category module'
    module = 'activity_category'


def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            ActivityCategoryTestCase))
    return suite

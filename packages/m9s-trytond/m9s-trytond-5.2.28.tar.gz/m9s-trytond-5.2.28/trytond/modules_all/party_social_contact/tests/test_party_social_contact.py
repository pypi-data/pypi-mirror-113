# This file is part of the party_social_contact module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class PartySocialContactTestCase(ModuleTestCase):
    'Test Party Social Contact module'
    module = 'party_social_contact'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PartySocialContactTestCase))
    return suite

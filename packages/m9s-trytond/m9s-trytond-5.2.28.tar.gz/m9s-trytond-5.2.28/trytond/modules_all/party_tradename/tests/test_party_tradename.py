# This file is part of the party_tradename module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class PartyTradenameTestCase(ModuleTestCase):
    'Test Party Tradename module'
    module = 'party_tradename'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PartyTradenameTestCase))
    return suite

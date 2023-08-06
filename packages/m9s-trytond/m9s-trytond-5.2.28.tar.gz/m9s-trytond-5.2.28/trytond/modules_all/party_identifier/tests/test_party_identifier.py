# This file is part of the party_identifier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class PartyIdentifierTestCase(ModuleTestCase):
    'Test Party Identifier module'
    module = 'party_identifier'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PartyIdentifierTestCase))
    return suite

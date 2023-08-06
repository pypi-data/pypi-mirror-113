#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class PartyAsteriskTestCase(ModuleTestCase):
    '''
    Test Party Asterisk module.
    '''
    module = 'party_asterisk'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PartyAsteriskTestCase))
    return suite

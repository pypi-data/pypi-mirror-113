# This file is part of the party_search module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool


class PartySearchTestCase(ModuleTestCase):
    'Test Party Search module'
    module = 'party_search'

    @with_transaction()
    def test_search(self):
        'Search party and addresses'
        pool = Pool()
        Party = pool.get('party.party')
        Address = pool.get('party.address')

        party1, = Party.create([{
                    'name': 'Party 1',
                    'addresses': [('create', [{
                        'street': 'Street 1',
                        'city': 'Vilafranca',
                        'zip': '08720',
                        }, {
                        'street': 'Street 2',
                        'city': 'Sabadell',
                        'zip': '08202',
                        }])],
                    'contact_mechanisms': [('create', [{
                        'type': 'phone',
                        'value': '+442083661177',
                        }])],
                    }])
        party2, = Party.create([{
                    'name': 'Party 2',
                    'addresses': [('create', [{
                        'street': 'Street 1',
                        'city': 'Manresa',
                        'zip': '08240',
                        }, {
                        'street': 'Street 2',
                        'city': 'Sabadell',
                        'zip': '08202',
                        }])],
                    'contact_mechanisms': [('create', [{
                        'type': 'phone',
                        'value': '+442083661166',
                        }])],
                    }])

        search1 = Address.search([('rec_name', 'ilike', '%sabadell%')])
        self.assertEqual(len(search1), 2)
        search2 = Party.search([('rec_name', 'ilike', '%sabadell%')])
        self.assertEqual(len(search2), 2)
        search3 = Party.search([('rec_name', 'ilike', '%+442083661166%')])
        self.assertEqual(len(search3), 1)
        search4 = Address.search([('rec_name', 'ilike', '%+442083661166%')])
        self.assertEqual(len(search4), 2)
        search5 = Address.search([
            ('rec_name', 'ilike', '%Party 1%'), ('zip', '=', '08202')])
        self.assertEqual(len(search5), 1)
        search6 = Address.search(['OR',
            ('rec_name', 'ilike', '%sabadell%'), ('zip', '=', '08720')])
        self.assertEqual(len(search6), 3)

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        PartySearchTestCase))
    return suite

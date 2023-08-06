# This file is part party_maps module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import unittest
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.pool import Pool


class PartyMapsTestCase(ModuleTestCase):
    'Test Party Maps module'
    module = 'party_maps'

    @with_transaction()
    def test_maps(self):
        "Test Maps"
        pool = Pool()
        Party = pool.get('party.party')
        Address = pool.get('party.address')

        party = Party()
        party.name = 'NaN-tic'
        party.save()

        address = Address()
        address.party = party
        address.street = "Carrer de les Paus, 98"
        address.zip = "08202"
        address.city = "Sabadell"
        address.map_place =  "Carrer de les Paus, 98 08202 Sabadell"
        address.save()
        Address.geocode([address])
        self.assertEqual('%s' % address.latitude, '41.5513006')
        self.assertEqual('%s' % address.longitude, '2.1130782')
        self.assertEqual(
            address.on_change_with_map_url(),
            'https://www.openstreetmap.org/search?'
            'query=41.55130060%2C2.11307820')

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            PartyMapsTestCase))
    return suite

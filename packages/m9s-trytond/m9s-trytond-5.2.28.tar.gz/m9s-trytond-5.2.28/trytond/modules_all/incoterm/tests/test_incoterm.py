# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.modules.company.tests import create_company, set_company


class IncotermTestCase(ModuleTestCase):
    'Test Incoterm module'
    module = 'incoterm'

    @with_transaction()
    def test_incoterm(self):
        'Incoterm'
        pool = Pool()
        Party = pool.get('party.party')
        Incoterm = pool.get('incoterm')

        company = create_company(name='Company 1')
        with set_company(company):
            incoterm, = Incoterm.search([('code', '=', 'EXW')], limit=1)
            party1, = Party.create([{
                        'name': 'Party 1',
                        'incoterm': incoterm,
                        'incoterm_place': 'Test1',
                        }])
            self.assertEqual(party1.incoterm, incoterm)
            party1_id = party1.id

        company = create_company(name='Company 2')
        with set_company(company):
            incoterm2, = Incoterm.search([('code', '=', 'FCA')], limit=1)
            party1 = Party(party1_id)
            party1.incoterm = incoterm2
            party1.save()
            self.assertEqual(party1.incoterm, incoterm2)
            self.assertEqual(party1.incoterm_place, None)

def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        IncotermTestCase))
    return suite

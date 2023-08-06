# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class SaleOpportunityCompetitorTestCase(ModuleTestCase):
    'Test Sale Opportunity Competitor module'
    module = 'sale_opportunity_competitor'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            SaleOpportunityCompetitorTestCase))
    return suite

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class AssetRelationshipTestCase(ModuleTestCase):
    'Test Asset Relationship module'
    module = 'asset_relationship'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AssetRelationshipTestCase))
    return suite

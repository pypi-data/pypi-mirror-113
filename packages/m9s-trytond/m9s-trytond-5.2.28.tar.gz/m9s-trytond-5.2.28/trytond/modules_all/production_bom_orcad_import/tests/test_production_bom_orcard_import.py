# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
# import doctest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProductionBomOrcadImport(ModuleTestCase):
    'Test module'
    module = 'production_bom_orcad_import'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductionBomOrcadImport
    ))
    return suite

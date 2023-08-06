# This file is part of the jasper_reports_options module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class JasperReportsOptionsTestCase(ModuleTestCase):
    'Test Jasper Reports Options module'
    module = 'jasper_reports_options'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        JasperReportsOptionsTestCase))
    return suite

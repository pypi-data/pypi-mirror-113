# This file is part of the project_state_by_buttons module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProjectStateByButtonsTestCase(ModuleTestCase):
    'Test Project State By Buttons module'
    module = 'project_state_by_buttons'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProjectStateByButtonsTestCase))
    return suite
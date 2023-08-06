# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProjectMenuRemoveTestCase(ModuleTestCase):
    'Test ProjectMenuRemove module'
    module = 'project_menu_tree_remove'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProjectMenuRemoveTestCase))
    return suite

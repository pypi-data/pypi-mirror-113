# This file is part of the project_timesheet module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase


class ProjectTimesheetTestCase(ModuleTestCase):
    'Test Project Timesheet module'
    module = 'project_timesheet'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProjectTimesheetTestCase))
    return suite
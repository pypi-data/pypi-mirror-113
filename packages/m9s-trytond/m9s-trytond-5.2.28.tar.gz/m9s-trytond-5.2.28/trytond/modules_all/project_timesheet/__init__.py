# This file is part project_timesheet module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import work

def register():
    Pool.register(
        work.WorkOpenTimesheetLine,
        work.WorkOpenAllTimesheetLine,
        module='project_timesheet', type_='wizard')

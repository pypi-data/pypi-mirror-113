# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import leave


def register():
    Pool.register(
        leave.Type,
        leave.Period,
        leave.Leave,
        leave.Entitlement,
        leave.Payment,
        leave.Employee,
        leave.EmployeeSummary,
        module='employee_leave', type_='model')

# This file is part account_code_digits module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

from trytond.pool import Pool
from . import account


def register():
    Pool.register(
        account.Configuration,
        account.ConfigurationDefaultAccount,
        account.AccountTemplate,
        account.Account,
        account.CreateChartAccount,
        account.UpdateChartStart,
        module='account_code_digits', type_='model')
    Pool.register(
        account.CreateChart,
        account.UpdateChart,
        module='account_code_digits', type_='wizard')

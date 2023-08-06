# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import account


def register():
    Pool.register(
        account.Payment,
        module='account_payment_receipt', type_='model')
    Pool.register(
        account.Receipt,
        module='account_payment_receipt', type_='report')

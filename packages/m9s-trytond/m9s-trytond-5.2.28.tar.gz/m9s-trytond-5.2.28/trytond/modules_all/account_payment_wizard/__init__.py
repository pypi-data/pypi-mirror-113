# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import Pool
from . import payment


def register():
    Pool.register(
        payment.PayLineAskJournal,
        module='account_payment_wizard', type_='model')
    Pool.register(
        payment.PayLine,
        module='account_payment_wizard', type_='wizard')

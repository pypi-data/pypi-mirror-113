# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .invoice import *


def register():
    Pool.register(
        PostInvoicesStart,
        module='account_invoice_post_wizard', type_='model')
    Pool.register(
        PostInvoices,
        module='account_invoice_post_wizard', type_='wizard')

# This file is part of the account_invoice_visible_payments module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import invoice


def register():
    Pool.register(
        invoice.Invoice,
        module='account_invoice_visible_payments', type_='model')

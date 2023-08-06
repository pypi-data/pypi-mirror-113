# This file is part commission_invoice_date module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import commission

def register():
    Pool.register(
        commission.Plan,
        commission.InvoiceLine,
        module='commission_invoice_date', type_='model')

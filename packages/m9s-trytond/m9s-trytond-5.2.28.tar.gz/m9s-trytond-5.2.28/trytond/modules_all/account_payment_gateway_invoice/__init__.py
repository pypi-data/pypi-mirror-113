# This file is part account_payment_gateway_invoice module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import gateway
from . import invoice


def register():
    Pool.register(
        gateway.AccountPaymentGatewayTransaction,
        invoice.Invoice,
        module='account_payment_gateway_invoice', type_='model')

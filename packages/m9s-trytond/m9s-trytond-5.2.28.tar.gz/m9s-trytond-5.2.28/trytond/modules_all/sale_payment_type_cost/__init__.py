# This file is part of sale_payment_type_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .sale import *
from .payment_type import *


def register():
    Pool.register(
        Sale,
        PaymentType,
        module='sale_payment_type_cost', type_='model')

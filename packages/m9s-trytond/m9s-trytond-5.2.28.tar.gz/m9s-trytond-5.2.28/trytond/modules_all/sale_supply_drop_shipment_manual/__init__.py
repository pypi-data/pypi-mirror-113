# This file is part sale_supply_drop_shipment_manual module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import sale

def register():
    Pool.register(
        sale.SaleLine,
        module='sale_supply_drop_shipment_manual', type_='model')

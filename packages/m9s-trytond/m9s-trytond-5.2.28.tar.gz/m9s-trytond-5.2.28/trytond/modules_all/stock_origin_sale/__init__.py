# This file is part stock_origin_sale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import sale
from . import shipment


def register():
    Pool.register(
        sale.Sale,
        shipment.ShipmentOut,
        shipment.ShipmentOutReturn,
        module='stock_origin_sale', type_='model')

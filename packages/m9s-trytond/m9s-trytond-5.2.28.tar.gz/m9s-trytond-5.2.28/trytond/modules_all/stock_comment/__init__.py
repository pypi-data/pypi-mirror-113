# This file is part stock_comment module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import company
from . import shipment
from . import party


def register():
    Pool.register(
        company.Company,
        shipment.ShipmentIn,
        shipment.ShipmentInReturn,
        shipment.ShipmentOut,
        shipment.ShipmentOutReturn,
        shipment.ShipmentInternal,
        party.Party,
        party.Address,
        module='stock_comment', type_='model')

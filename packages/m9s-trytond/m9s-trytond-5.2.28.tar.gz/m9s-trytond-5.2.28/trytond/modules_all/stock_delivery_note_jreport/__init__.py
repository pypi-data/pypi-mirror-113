# This file is part stock_delivery_note_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import configuration
from . import shipment


def register():
    Pool.register(
        configuration.Configuration,
        configuration.StockConfigurationCompany,
        module='stock_delivery_note_jreport', type_='model'),
    Pool.register(
        shipment.DeliveryNote,
        shipment.PickingList,
        shipment.DeliveryNoteReturn,
        shipment.DeliveryNoteValued,
        module='stock_delivery_note_jreport', type_='report')

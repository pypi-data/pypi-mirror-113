# This file is part stock_delivery_note_valued_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import shipment


def register():
    Pool.register(
        shipment.DeliveryNoteValued,
        module='stock_delivery_note_valued_jreport', type_='report')

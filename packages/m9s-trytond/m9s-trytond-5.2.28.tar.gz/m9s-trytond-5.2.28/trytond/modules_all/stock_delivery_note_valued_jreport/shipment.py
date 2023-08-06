# This file is part stock_delivery_note_valuer_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.modules.jasper_reports.jasper import JasperReport

__all__ = ['DeliveryNoteValued']


class DeliveryNoteValued(JasperReport):
    __name__ = 'stock.shipment.out.delivery_note_valued'

    @classmethod
    def execute(cls, ids, data):
        pool = Pool()
        Config = pool.get('stock.configuration')

        config = Config(1)
        parameters = {
            'shipment_qty_decimal': config.shipment_qty_decimal or False
            }
        if 'parameters' in data:
            data['parameters'].update(parameters)
        else:
            data['parameters'] = parameters
        return super(DeliveryNoteValued, cls).execute(ids, data)

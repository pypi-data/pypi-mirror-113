# This file is part stock_delivery_note_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from trytond.pool import PoolMeta
from trytond.modules.jasper_reports.jasper import JasperReport

__all__ = ['DeliveryNote', 'PickingList', 'DeliveryNoteReturn',
    'DeliveryNoteValued']


class DeliveryNote(JasperReport, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.delivery_note'

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
        return super(DeliveryNote, cls).execute(ids, data)


class PickingList(JasperReport, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.picking_list'

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
        return super(PickingList, cls).execute(ids, data)


class DeliveryNoteReturn(JasperReport, metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.delivery_note.return'

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
        return super(DeliveryNoteReturn, cls).execute(ids, data)


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

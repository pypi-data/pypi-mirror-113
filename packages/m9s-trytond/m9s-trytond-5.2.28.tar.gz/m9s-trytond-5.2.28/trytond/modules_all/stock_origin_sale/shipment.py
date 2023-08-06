# This file is part stock_origin_sale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentOut', 'ShipmentOutReturn']


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    @classmethod
    def get_origin_value(cls, shipments, name):
        SaleLine = Pool().get('sale.line')

        origin = super(ShipmentOut, cls).get_origin_value(shipments, name)
        for shipment in shipments:
            if shipment.origin_cache:
                origin[shipment.id] = '%s' % shipment.origin_cache
                continue

            for m in shipment.outgoing_moves:
                if m.origin and isinstance(m.origin, SaleLine):
                    origin[shipment.id] = 'sale.sale,%s' % (m.origin.sale.id)
                    break
        return origin

    @classmethod
    def _get_origin(cls):
        return super(ShipmentOut, cls)._get_origin() + ['sale.sale']

    @classmethod
    def _get_searcher_number(cls):
        return super(ShipmentOut, cls)._get_searcher_number() + ['sale.sale']

    @classmethod
    def _get_searcher_reference(cls):
        return super(ShipmentOut, cls)._get_searcher_reference() + [
            'sale.sale']


class ShipmentOutReturn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out.return'

    @classmethod
    def get_origin_value(cls, shipments, name):
        SaleLine = Pool().get('sale.line')

        origin = super(ShipmentOutReturn, cls).get_origin_value(
            shipments, name)
        for shipment in shipments:
            if shipment.origin_cache:
                origin[shipment.id] = '%s' % shipment.origin_cache
                continue

            for m in shipment.incoming_moves:
                if m.origin and isinstance(m.origin, SaleLine):
                    origin[shipment.id] = 'sale.sale,%s' % (m.origin.sale.id)
                    break
        return origin

    @classmethod
    def _get_origin(cls):
        return super(ShipmentOutReturn, cls)._get_origin() + ['sale.sale']

    @classmethod
    def _get_searcher_number(cls):
        return super(ShipmentOutReturn, cls)._get_searcher_number() + [
            'sale.sale']

    @classmethod
    def _get_searcher_reference(cls):
        return super(ShipmentOutReturn, cls)._get_searcher_reference() + [
            'sale.sale']

# This file is part of the stock_origin_sale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    def _get_shipment_sale(self, Shipment, key):
        key += (('origin', self),)
        return super(Sale, self)._get_shipment_sale(Shipment, key)

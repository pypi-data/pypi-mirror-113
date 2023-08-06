# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import order_point
from . import ir
from . import product
from . import purchase_request
from . import shipment
from . import location
from . import stock

__all__ = ['register']


def register():
    Pool.register(
        order_point.OrderPoint,
        product.Product,
        product.ProductSupplier,
        purchase_request.PurchaseConfiguration,
        purchase_request.PurchaseConfigurationSupplyPeriod,
        purchase_request.PurchaseRequest,
        shipment.ShipmentInternal,
        location.Location,
        location.LocationLeadTime,
        stock.StockSupplyStart,
        ir.Cron,
        module='stock_supply', type_='model')
    Pool.register(
        stock.StockSupply,
        module='stock_supply', type_='wizard')

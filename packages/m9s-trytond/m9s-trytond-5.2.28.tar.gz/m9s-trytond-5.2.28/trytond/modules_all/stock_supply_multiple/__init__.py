# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import purchase


def register():
    Pool.register(
        purchase.ProductSupplier,
        purchase.PurchaseRequest,
        module='stock_supply_multiple', type_='model')
    Pool.register(
        purchase.CreatePurchase,
        module='stock_supply_multiple', type_='wizard')

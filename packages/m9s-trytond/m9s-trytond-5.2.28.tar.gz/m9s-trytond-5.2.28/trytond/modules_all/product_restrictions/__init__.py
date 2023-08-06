# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product
from . import party


def register():
    Pool.register(
        product.Restriction,
        product.RestrictionTemplate,
        product.Template,
        module='product_restrictions', type_='model')
    Pool.register(
        party.RestrictionCustomer,
        party.PartyCustomer,
        product.Sale,
        product.ShipmentOut,
        product.ShipmentOutReturn,
        depends=['sale'],
        module='product_restrictions', type_='model')
    Pool.register(
        party.RestrictionSupplier,
        party.PartySupplier,
        product.Purchase,
        product.ShipmentIn,
        depends=['purchase'],
        module='product_restrictions', type_='model')

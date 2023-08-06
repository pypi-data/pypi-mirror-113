# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product


def register():
    Pool.register(
        product.Template,
        module='product_validate', type_='model')
    Pool.register(
        product.InvoiceLine,
        depends=['account_invoice'],
        module='product_validate', type_='model')
    Pool.register(
        product.PurchaseLine,
        depends=['purchase'],
        module='product_validate', type_='model')
    Pool.register(
        product.SaleLine,
        depends=['sale'],
        module='product_validate', type_='model')

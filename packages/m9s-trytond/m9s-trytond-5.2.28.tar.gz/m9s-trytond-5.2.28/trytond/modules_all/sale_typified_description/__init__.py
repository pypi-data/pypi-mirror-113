# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import typified
from . import sale


def register():
    Pool.register(
        typified.Category,
        typified.Description,
        sale.SaleTypifiedDescription,
        sale.SaleLineTypifiedDescription,
        sale.Sale,
        sale.SaleLine,
        module='sale_typified_description', type_='model')

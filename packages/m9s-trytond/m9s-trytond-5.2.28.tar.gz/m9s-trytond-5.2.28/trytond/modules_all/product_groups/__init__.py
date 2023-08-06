# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import product


def register():
    Pool.register(
        product.Group,
        product.GroupTemplate,
        product.Template,
        module='product_groups', type_='model')

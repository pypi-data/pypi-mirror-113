# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import PoolMeta

__all__ = ['Sale', 'SaleTypifiedDescription', 'SaleLine',
    'SaleLineTypifiedDescription']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    terms = fields.Many2Many('sale.order-typified.description', 'sale',
        'description', 'Sale Terms')


class SaleTypifiedDescription(ModelSQL):
    'Sale Order - Typified Description'
    __name__ = 'sale.order-typified.description'

    sale = fields.Many2One('sale.sale', 'Sale', ondelete='CASCADE',
        required=True, select=True)
    description = fields.Many2One('typified.description', 'Term',
        ondelete='CASCADE', required=True, select=True)


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    terms = fields.Many2Many('sale.line-typified.description', 'line',
        'description', 'Sale term')


class SaleLineTypifiedDescription(ModelSQL):
    'Sale Line - Typified Description'
    __name__ = 'sale.line-typified.description'

    line = fields.Many2One('sale.line', 'Sale Line', ondelete='CASCADE',
        required=True, select=True)
    description = fields.Many2One('typified.description', 'Term',
        ondelete='CASCADE', required=True, select=True)

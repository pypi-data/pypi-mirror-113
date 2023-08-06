# This file is part sale_external_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.config import config as config_

__all__ = ['Sale']

DIGITS = config_.getint('product', 'price_decimal', default=4)
DISCOUNT_DIGITS = config_.getint('product', 'discount_decimal', default=4)


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    external_untaxed_amount = fields.Numeric('External Untaxed',
        readonly=True, digits=(16, DIGITS))
    external_tax_amount = fields.Numeric('External Tax',
        readonly=True, digits=(16, DIGITS))
    external_total_amount = fields.Numeric('External Total',
        readonly=True, digits=(16, DIGITS))
    external_shipment_amount = fields.Numeric('External Total Shipment',
        readonly=True, digits=(16, DIGITS))
    external_discount = fields.Numeric('External Discount',
        readonly=True, digits=(16, DISCOUNT_DIGITS))

    @classmethod
    def view_attributes(cls):
        return super(Sale, cls).view_attributes() + [
            ('//page[@id="other"]/group[@id="external_price"]', 'states', {
                    'invisible': ~Eval('external_untaxed_amount'),
                    })]

# This file is part of the stock_comment module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Party', 'Address']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    comment_shipment = fields.Text('Shipment Comment')


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'
    comment_shipment = fields.Text('Shipment Comment',
        states={
            'invisible': ~Eval('delivery', True),
            }, depends=['delivery'])

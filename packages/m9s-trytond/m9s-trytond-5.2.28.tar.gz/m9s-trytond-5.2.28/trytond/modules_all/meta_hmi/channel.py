# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.model import fields

STATES = {
    'readonly': ~Eval('active', True),
    }
DEPENDS = ['active']


class SaleChannel(metaclass=PoolMeta):
    __name__ = 'sale.channel'

    free_shipping_limit = fields.Numeric('Free shipment above',
        help='If the net amount of the order exceeds this setting '
        'the shipment will be free for the customer.',
        states=STATES, depends=DEPENDS)

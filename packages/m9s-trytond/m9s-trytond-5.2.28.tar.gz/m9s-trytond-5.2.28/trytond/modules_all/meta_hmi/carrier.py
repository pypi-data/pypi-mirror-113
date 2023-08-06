# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal

from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from trytond.model import fields


class Carrier(metaclass=PoolMeta):
    __name__ = "carrier"

    comment = fields.Text('Comment',
        help='Internal comments for this carrier')
    delivery_comment = fields.Char('Delivery comment',
        help='For display on the website, e.g. expected delivery time')
    service_type = fields.Function(fields.Char('Service Type'),
        'get_service_type')

    @classmethod
    def __setup__(cls):
        super(Carrier, cls).__setup__()
        #cls._order = [('rec_name', 'ASC')]
        cls._order = [('party', 'ASC'), ('carrier_product.rec_name', 'ASC')]

    def get_rec_name(self, name):
        field_names = [
            self.party.rec_name,
            self.carrier_product.rec_name,
            self.service_type,
            ]
        return ' - '.join(filter(None, field_names))

    @classmethod
    def get_service_type(cls, records, name=None):
        '''
        Return the selection value of fields *_service_type
        '''
        res = {}
        for record in records:
            res[record.id] = [dict(cls.fields_get([f])[f]['selection'])[
                    getattr(record, f, None)] for f in cls._fields
                if f.endswith('_service_type')][0]
        return res

    def get_sale_price(self):
        '''
        Part of our internal implementation for free shipping.
        '''
        pool = Pool()
        Currency = pool.get('currency.currency')
        Company = pool.get('company.company')
        Sale = pool.get('sale.sale')

        shipping_cost = super(Carrier, self).get_sale_price()
        if self.carrier_cost_method == 'weight_volume':
            company = Transaction().context.get('company')
            if company:
                currency = Company(company).currency
            else:
                currency, = Currency.search([('code', '=', 'EUR')])
            sale_id = Transaction().context.get('sale')
            sale = Sale(sale_id) if sale_id else None
            if sale and sale.get_free_shipping():
                # Free shipping only for XS and S packages
                if shipping_cost[0] > Decimal('8.0'):
                    return shipping_cost
                else:
                    return Decimal('0.0'), currency.id
        return shipping_cost

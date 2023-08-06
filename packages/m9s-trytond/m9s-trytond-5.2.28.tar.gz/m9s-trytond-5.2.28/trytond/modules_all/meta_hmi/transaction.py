# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class PaymentGateway(metaclass=PoolMeta):
    __name__ = 'payment_gateway.gateway'

    defer_payment = fields.Boolean('Defer Payment',
        help='Do not create any automatic payment for this gateway.')


class PaymentTransaction(metaclass=PoolMeta):
    __name__ = 'payment_gateway.transaction'

    def get_rec_name(self, name=None):
        '''
        payment_gateway
          - Provide a rec_name stripped from None elements
        '''
        if self.state == 'draft':
            return self.uuid
        rec_name = ''
        if self.payment_profile:
            rec_name += self.payment_profile.rec_name
        else:
            rec_name += self.gateway.name
        reference = self.provider_reference or ''
        if reference:
            rec_name += '/%s' % (reference,)
        return rec_name

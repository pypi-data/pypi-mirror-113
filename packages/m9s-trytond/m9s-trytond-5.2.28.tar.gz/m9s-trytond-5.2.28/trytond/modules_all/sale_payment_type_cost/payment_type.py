# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Bool, Eval, Not, Or

__all__ = ['PaymentType']


class PaymentType(metaclass=PoolMeta):
    __name__ = 'account.payment.type'
    exclude_shipment_lines = fields.Boolean('Exclude Shipment Lines',
        states={
            'invisible': Or(Bool(Eval('compute_over_total_amount')),
                Not(Bool(Eval('has_cost')))),
                },
        help='Excludes the shipment lines of computation of costs of this '
            'payment type.')

    @fields.depends('compute_over_total_amount')
    def on_change_compute_over_total_amount(self):
        try:
            super(PaymentType, self).on_change_compute_over_total_amount()
        except AttributeError:
            pass
        if self.compute_over_total_amount:
            self.exclude_shipment_lines = False

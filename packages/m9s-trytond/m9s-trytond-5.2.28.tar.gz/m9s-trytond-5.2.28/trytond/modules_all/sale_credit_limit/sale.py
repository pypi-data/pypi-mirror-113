# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, Workflow
from trytond.pool import PoolMeta
from trytond.transaction import Transaction

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    @ModelView.button
    @Workflow.transition('confirmed')
    def confirm(cls, sales):
        if not Transaction().context.get('skip_credit_check'):
            for sale in sales:
                if (sale.state == 'quotation'
                        and sale.shipment_method == 'order'):
                    sale.party.check_credit_limit(sale.untaxed_amount,
                        origin=str(sale))
        return super(Sale, cls).confirm(sales)

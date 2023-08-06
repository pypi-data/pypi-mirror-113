# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['InvoiceLine']


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'
    invoice_asset = fields.Many2One('asset', 'Asset',
        states={
            'invisible': Eval('type') != 'line',
            },
        depends=['type'])

    def _credit(self):
        credit = super(InvoiceLine, self)._credit()
        credit.invoice_asset = self.invoice_asset
        return credit

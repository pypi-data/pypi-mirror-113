# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['PurchaseLine']


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    def get_invoice_line(self):
        lines = super(PurchaseLine, self).get_invoice_line()
        if self.purchase.invoice_method == 'shipment':
            for line in lines:
                if line.stock_moves:
                    line.unit_price = line.stock_moves[0].unit_price
        return lines

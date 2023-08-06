# This file is part of sale_payment_type_cost module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

__all__ = ['Sale']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def quote(cls, sales):
        pool = Pool()
        Line = pool.get('sale.line')

        super(Sale, cls).quote(sales)

        for sale in sales:
            if sale.payment_type and sale.payment_type.has_cost:
                lines = Line.search([
                        ('sale', '=', sale),
                        ('product', '=', sale.payment_type.cost_product),
                        ])
                if lines:
                    Line.delete(lines)
                line = sale._get_payment_type_cost_line()
                line.save()

    def _get_payment_type_cost_line(self):
        " Returns sale line with the cost"
        pool = Pool()
        Line = pool.get('sale.line')

        line = Line()
        line.sale = self
        for key, value in Line.default_get(list(Line._fields.keys()),
                with_rec_name=False).items():
            if value is not None:
                setattr(line, key, value)
        line.quantity = 1
        line.product = self.payment_type.cost_product
        line.on_change_product()
        if self.payment_type.compute_over_total_amount:
            amount = self.total_amount
        elif self.payment_type.exclude_shipment_lines:
            amount = sum([l.amount
                    for l in self.lines
                    if not getattr(l, 'shipment_cost', False)
                    ])
        else:
            amount = self.untaxed_amount
        unit_price = (amount * self.payment_type.cost_percent)
        line.unit_price = unit_price
        # compatibility with sale discount
        if hasattr(line, 'gross_unit_price'):
            line.gross_unit_price = unit_price
            line.update_prices()
        return line

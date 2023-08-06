# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import stock


def register():
    Pool.register(
        stock.Move,
        module='stock_move_label', type_='model')
    Pool.register(
        stock.MoveLabel,
        module='stock_move_label', type_='report')

# This file is part of stock_move_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import move

def register():
    Pool.register(
        move.MoveReport,
        module='stock_move_jreport', type_='report')

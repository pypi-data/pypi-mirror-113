# This file is part account_move_draft module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import move

def register():
    Pool.register(
        move.Move,
        module='account_move_draft', type_='model')

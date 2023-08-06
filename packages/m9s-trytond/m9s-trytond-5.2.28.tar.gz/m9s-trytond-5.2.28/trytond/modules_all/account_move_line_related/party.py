#This file is part of account_move_line_related module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Party']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    receivable_lines = fields.Function(fields.One2Many('account.move.line',
            None, 'Receivable Lines'), 'get_receivable_payable_lines')
    payable_lines = fields.Function(fields.One2Many('account.move.line',
            None, 'Payable Lines'), 'get_receivable_payable_lines')

    def get_receivable_payable_lines(self, name):
        '''
        Function to compute receivable, payable not reconcilied lines for party
        '''
        pool = Pool()
        MoveLine = pool.get('account.move.line')

        if name not in ('receivable_lines', 'payable_lines'):
            raise Exception('Bad argument')
        lines = MoveLine.search([
                ('party', '=', self.id),
                ('account.kind', '=', name[:-6]),
                ('reconciliation', '=', None)])
        return [l.id for l in lines]

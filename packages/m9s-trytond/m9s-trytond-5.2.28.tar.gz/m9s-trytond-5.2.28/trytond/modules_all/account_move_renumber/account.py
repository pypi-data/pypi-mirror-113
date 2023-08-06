# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import PYSONEncoder
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.i18n import gettext
from trytond.exceptions import UserError, UserWarning

__all__ = ['Move', 'RenumberMoves', 'RenumberMovesStart']


class Move(metaclass=PoolMeta):
    __name__ = 'account.move'

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()
        if 'post_number' not in cls._check_modify_exclude:
            cls._check_modify_exclude.append('post_number')


class RenumberMovesStart(ModelView):
    '''Renumber Account Moves Start'''
    __name__ = 'account.move.renumber.start'

    fiscalyear = fields.Many2One('account.fiscalyear', 'Fiscal Year',
        required=True)
    first_number = fields.Integer('First Number', required=True,
        domain=[('first_number', '>', 0)])

    @staticmethod
    def default_first_number():
        return 1


class RenumberMoves(Wizard):
    '''Renumber Account Moves'''
    __name__ = 'account.move.renumber'

    start = StateView('account.move.renumber.start',
        'account_move_renumber.move_renumber_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Renumber', 'renumber', 'tryton-ok', default=True),
            ])
    renumber = StateAction('account.act_move_form')

    def do_renumber(self, action):
        pool = Pool()
        Move = pool.get('account.move')
        Sequence = pool.get('ir.sequence')
        Warning = pool.get('res.user.warning')
        draft_moves = Move.search([
                ('period.fiscalyear', '=', self.start.fiscalyear.id),
                ('state', '=', 'draft'),
                ])
        if draft_moves:
            key = 'move_renumber_draft_moves%s' % self.start.fiscalyear.id
            if Warning.check(key):
                raise UserWarning(key,
                    gettext('account_move_renumber.draft_moves_in_fiscalyear',
                        fiscalyear=self.start.fiscalyear.rec_name))

        sequences = set([self.start.fiscalyear.post_move_sequence])
        for period in self.start.fiscalyear.periods:
            if period.post_move_sequence:
                sequences.add(period.post_move_sequence)

        Sequence.write(list(sequences), {
                'number_next': self.start.first_number,
                })

        moves_to_renumber = Move.search([
                ('period.fiscalyear', '=', self.start.fiscalyear.id),
                ('post_number', '!=', None),
                ],
            order=[
                ('date', 'ASC'),
                ('id', 'ASC'),
                ])
        move_vals = []
        for move in moves_to_renumber:
            move_vals.extend(([move], {
                        'post_number': Sequence.get_id(
                            move.period.post_move_sequence_used.id),
                        }))
        Move.write(*move_vals)

        action['pyson_domain'] = PYSONEncoder().encode([
            ('period.fiscalyear', '=', self.start.fiscalyear.id),
            ('post_number', '!=', None),
            ])
        return action, {}

    def transition_renumber(self):
        return 'end'

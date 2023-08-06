# This file is part of account_reconcile_different_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Line', 'Reconciliation']


class Line(metaclass=PoolMeta):
    __name__ = 'account.move.line'

    @classmethod
    def __setup__(cls):
        super(Line, cls).__setup__()
        if cls.party.states.get('invisible'):
            cls.party.states.pop('invisible')

    @fields.depends('party')
    def on_change_account(self):
        party = self.party
        super(Line, self).on_change_account()
        # Not remove party if account is not party required
        if party:
            self.party = party

    def check_account(self):
        try:
            super(Line, self).check_account()
        except:
            # Not raise if there is a party and account is not party required
            if self.account.party_required or not self.party:
                raise


class Reconciliation(metaclass=PoolMeta):
    __name__ = 'account.move.reconciliation'


    @classmethod
    def check_lines(cls, reconciliations):
        for reconciliation in reconciliations:
            if reconciliation.lines:
                party = reconciliation.lines[0].party

            for line in reconciliation.lines:
                if line.account.different_party_reconcile:
                    line.party = None
                elif line.party and line.party != party:
                    raise UserError(gettext(
                    'account_reconcile_different_party.reconciliation_has_party',
                            line=line.rec_name,
                            account=line.account.rec_name,
                            party=line.party.rec_name,
                            ))
        super(Reconciliation, cls).check_lines(reconciliations)

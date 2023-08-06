# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Invoice', 'Party']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    send_in_paper = fields.Function(fields.Boolean('Send in paper'),
        'get_send_in_paper', searcher='search_send_in_paper')

    def get_send_in_paper(self, name):
        return self.party.send_in_paper

    @classmethod
    def search_send_in_paper(cls, name, clause):
        return [('party.send_in_paper',) + tuple(clause[1:])]


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    send_in_paper = fields.Boolean('Send in paper',
        help='Indicates whether the party wants to receive the invoice in '
        'paper or not.')

    @staticmethod
    def default_send_in_paper():
        return True

    @classmethod
    def validate(cls, parties):
        super(Party, cls).validate(parties)
        for party in parties:
            party.check_send_in_paper()

    def check_send_in_paper(self):
        if self.send_in_paper:
            return
        if not any(c.type == 'email' for c in self.contact_mechanisms):
            raise UserError(gettext(
                'account_invoice_send_in_paper.no_email_and_in_paper',
                    party=self.rec_name))

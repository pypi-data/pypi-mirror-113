# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import fields


class BatchLine(metaclass=PoolMeta):
    __name__ = 'account.batch.line'

    @fields.depends('invoice', 'date', 'batch', 'amount', 'journal')
    def on_change_invoice(self):
        pool = Pool()
        Account = pool.get('account.account')

        if self.invoice and self.invoice.state == 'paid':
            reference = self.invoice.reference or self.invoice.number
            self.reference = reference
            self.posting_text = reference
            account, = Account.search([
                    ('code', '=', '1360'),
                    ('id', '>', 138),   # Hack: only SKR03
                    ])
            self.contra_account = account.id
            self.party = self.invoice.party.id
            self.invoice = None
        else:
            super(BatchLine, self).on_change_invoice()

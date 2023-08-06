# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Invoice']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @fields.depends('party', 'agent')
    def on_change_party(self):
        super(Invoice, self).on_change_party()
        if self.party and self.party.agent and not self.agent:
            self.agent = self.party.agent

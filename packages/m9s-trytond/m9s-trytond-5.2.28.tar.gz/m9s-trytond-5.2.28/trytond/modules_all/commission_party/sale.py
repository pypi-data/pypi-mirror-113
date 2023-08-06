# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Sale', 'Opportunity']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    def set_agent_party(self, type='party'):
        if self.shipment_party:
            return True
        return False if self.agent else True

    @fields.depends('party', 'agent')
    def on_change_party(self):
        Config = Pool().get('sale.configuration')

        super(Sale, self).on_change_party()

        config = Config(1)
        agent_party = config.agent_party if config.agent_party else 'party'
        set_agent_party = self.set_agent_party(type=agent_party)

        if set_agent_party and getattr(self, agent_party):
            self.agent = getattr(self, agent_party).agent


class Opportunity(metaclass=PoolMeta):
    __name__ = 'sale.opportunity'

    def _get_sale_opportunity(self):
        Config = Pool().get('sale.configuration')

        sale = super(Opportunity, self)._get_sale_opportunity()

        config = Config(1)
        agent_party = config.agent_party if config.agent_party else 'party'

        if getattr(self, agent_party):
            sale.agent = getattr(self, agent_party).agent
        return sale

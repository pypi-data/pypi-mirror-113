# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from sql import Null
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond import backend
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)
from sql.operators import And

__all__ = ['Party', 'Agent', 'PartyCommissionAgent']


class Party(CompanyMultiValueMixin, metaclass=PoolMeta):
    __name__ = 'party.party'
    agents = fields.One2Many('party.party.commission.agent', 'party', 'Agents',
         domain=[
             ('company', '=', Eval('context', {}).get('company', -1)),
             ],
         states={
             'invisible': ~Eval('context', {}).get('company'),
             })
    agent = fields.MultiValue(fields.Many2One('commission.agent', 'Agent',
         domain=[
             ('company', '=', Eval('context', {}).get('company', -1)),
             ],
         states={
             'invisible': ~Eval('context', {}).get('company'),
             }))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field in {'agent'}:
            return pool.get('party.party.commission.agent')
        return super(Party, cls).multivalue_model(field)


class Agent(metaclass=PoolMeta):
    __name__ = 'commission.agent'
    assigned_parties = fields.Function(fields.One2Many('party.party', None,
        'Assigned Parties'), 'get_assigned_parties')

    @classmethod
    def copy(cls, agents, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default.setdefault('assigned_parties')
        return super(Agent, cls).copy(agents, default)

    def get_assigned_parties(self, name):
        pool = Pool()
        PartyCommissionAgent = pool.get('party.party.commission.agent')
        Party = pool.get('party.party')
        TableHandler = backend.get('TableHandler')
        party_company_exist = TableHandler.table_exist('party_company_rel')

        if party_company_exist:
            PartyCompany = pool.get('party.company.rel')
            party_company = PartyCompany.__table__()

        partyagent = PartyCommissionAgent.__table__()
        party = Party().__table__()
        cursor = Transaction().connection.cursor()

        join = partyagent.join(party, condition=partyagent.party == party.id)
        sql_where = ((partyagent.agent == self.id)
            & (partyagent.company == self.company.id) & (party.active == True))

        if party_company_exist:
            join = join.join(party_company,
                condition=partyagent.party == party_company.party)
            sql_where.append(And(party_company.company == self.company.id))

        cursor.execute(*join.select(partyagent.party, where=sql_where))
        ids = cursor.fetchall()
        if not ids:
            return []
        return [p[0] for p in ids]


class PartyCommissionAgent(ModelSQL, CompanyValueMixin):
    "Party Commission Agent"
    __name__ = 'party.party.commission.agent'
    party = fields.Many2One('party.party', "Party", ondelete='CASCADE',
        select=True)
    agent = fields.Many2One('commission.agent', 'Agent', domain=[
            ('company', '=', Eval('company', -1)),
            ],
        depends=['company'])

    @classmethod
    def __register__(cls, module_name):
        Party = Pool().get('party.party')
        TableHandler = backend.get('TableHandler')
        cursor = Transaction().connection.cursor()
        exist = TableHandler.table_exist(cls._table)
        table = cls.__table__()
        party = Party.__table__()

        super(PartyCommissionAgent, cls).__register__(module_name)

        if not exist:
            party_h = TableHandler(Party, module_name)
            if party_h.column_exist('agent'):
                query = table.insert(
                    [table.party, table.agent],
                    party.select(party.id, party.agent,
                        where=(party.agent != Null)))
                cursor.execute(*query)
                party_h.drop_column('agent')

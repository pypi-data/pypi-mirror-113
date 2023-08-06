# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import fields

__all__ = ['Plan', 'InvoiceLine']


class Plan(metaclass=PoolMeta):
    __name__ = 'commission.plan'
    invoice_date = fields.Boolean('Invoice Date',
        help='Create commissions with invoice date')


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    def get_commissions(self):
        Date = Pool().get('ir.date')

        commissions = super(InvoiceLine, self).get_commissions()

        today = Date.today()

        # get the commission with the agent_plans_used with position list
        agent_plans_used = self.agent_plans_used

        if not agent_plans_used:
            return commissions

        for commission in commissions:
            agent, plan = agent_plans_used.pop(0)
            if not plan:
                continue
            if plan.invoice_date:
                commission.date = self.invoice and self.invoice.invoice_date \
                    or today

        return commissions

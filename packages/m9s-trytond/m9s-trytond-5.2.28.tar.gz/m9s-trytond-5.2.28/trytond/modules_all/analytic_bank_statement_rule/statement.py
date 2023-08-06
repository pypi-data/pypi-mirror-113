# This file is part analytic_bank_statement_rule module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelView, ModelSQL, fields
from trytond.pyson import If, Eval

__all__ = ['StatementLineRuleLineAnalytic', 'StatementLineRuleLine',
    'StatementLine']


class StatementLineRuleLineAnalytic(ModelSQL, ModelView):
    'Statement Line Rule Line Analytic'
    __name__ = 'account.bank.statement.line.rule.line.analytic'
    rule_line = fields.Many2One('account.bank.statement.line.rule.line',
        'Rule Line', required=True)
    analytic_account = fields.Many2One('analytic_account.account',
        'Analytic Account', required=True, domain=[
            ('company', If(Eval('context', {}).contains('company'), '=', '!='),
            Eval('context', {}).get('company', -1)),
        ])


class StatementLineRuleLine(metaclass=PoolMeta):
    __name__ = 'account.bank.statement.line.rule.line'
    analytic_accounts = fields.One2Many(
        'account.bank.statement.line.rule.line.analytic', 'rule_line',
        'Analytic Accounts')


class StatementLine(metaclass=PoolMeta):
    __name__ = 'account.bank.statement.line'

    def get_move_line_from_rline(self, rline, amount):
        pool = Pool()
        AnalyticAccountEntry = pool.get('analytic.account.entry')
        mline = super(StatementLine, self).get_move_line_from_rline(rline,
            amount)
        analytic_accounts = [AnalyticAccountEntry(root=x.analytic_account.root,
                account=x.analytic_account) for x in rline.analytic_accounts]
        mline.analytic_accounts = analytic_accounts

        return mline

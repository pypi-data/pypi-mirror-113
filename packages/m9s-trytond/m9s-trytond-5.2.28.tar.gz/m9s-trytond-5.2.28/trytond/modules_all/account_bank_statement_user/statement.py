from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['StatementLine']


class StatementLine(metaclass=PoolMeta):
    __name__ = 'account.bank.statement.line'
    user = fields.Many2One('res.user', 'User')

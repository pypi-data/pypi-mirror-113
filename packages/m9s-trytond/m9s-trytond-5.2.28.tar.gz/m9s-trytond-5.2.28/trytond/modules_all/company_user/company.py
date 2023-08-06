# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Company']


class Company(metaclass=PoolMeta):
    __name__ = 'company.company'
    intercompany_user = fields.Many2One('res.user', 'Company User',
        help='User with company rules when create to other company.')

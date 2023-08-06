# This file is part of account_reconcile_different_party module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta


class Account(metaclass=PoolMeta):
    __name__ = 'account.account'

    different_party_reconcile = fields.Boolean(
        'Different Party Reconciliation',
        help='Allow move lines of this account to be reconciled despite '
        'having different party.')

    @staticmethod
    def default_different_party_reconcile():
        return False

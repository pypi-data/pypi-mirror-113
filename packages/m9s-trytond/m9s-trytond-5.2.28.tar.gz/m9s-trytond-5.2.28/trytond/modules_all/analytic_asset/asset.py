# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import fields

from trytond.modules.analytic_account import AnalyticMixin

__all__ = ['Asset', 'AnalyticAccountEntry']


class Asset(AnalyticMixin, metaclass=PoolMeta):
    __name__ = 'asset'


class AnalyticAccountEntry(metaclass=PoolMeta):
    __name__ = 'analytic.account.entry'

    @classmethod
    def _get_origin(cls):
        origins = super(AnalyticAccountEntry, cls)._get_origin()
        return origins + ['asset']

    @fields.depends('origin')
    def on_change_with_company(self, name=None):
        pool = Pool()
        Asset = pool.get('asset')
        company = super(AnalyticAccountEntry, self).on_change_with_company(
            name=name)
        if isinstance(self.origin, Asset):
            if self.origin.company:
                return self.origin.company.id
        return company

    @classmethod
    def search_company(cls, name, clause):
        domain = super(AnalyticAccountEntry, cls).search_company(name, clause)
        return ['OR',
            domain,
            [('origin.company',) + tuple(clause[1:]) + ('asset',)]
            ]

# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta


class Cron(metaclass=PoolMeta):
    __name__ = 'ir.cron'

    @classmethod
    def __setup__(cls):
        super().__setup__()
        cls.method.selection.extend([
                ('nereid.website|refresh_sitemap_cache',
                    'Refresh the sitemap cache'),
                ('sale.sale|delete_old_carts',
                    'Delete Old Carts'),
                ])

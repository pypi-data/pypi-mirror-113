# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Production']


class Production(metaclass=PoolMeta):
    __name__ = 'production'

    @classmethod
    def __setup__(cls):
        super(Production, cls).__setup__()
        # Ensure these fields have all the fields necessary for on_change in
        # the depends so productions are editable in tree view.
        for fname in ('product', 'quantity', 'planned_date'):
            field = getattr(cls, fname)
            if not field.on_change:
                continue
            for onchange_fname in field.on_change:
                if onchange_fname not in field.depends:
                    field.depends.append(onchange_fname)

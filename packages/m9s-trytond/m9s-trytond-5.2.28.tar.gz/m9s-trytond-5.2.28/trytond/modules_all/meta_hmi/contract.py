# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta


class Contract(metaclass=PoolMeta):
    __name__ = 'contract'

    def _get_rec_name(self, name):
        rec_name = super(Contract, self)._get_rec_name(name)
        if self.reference:
            rec_name.append(self.reference)
        return rec_name

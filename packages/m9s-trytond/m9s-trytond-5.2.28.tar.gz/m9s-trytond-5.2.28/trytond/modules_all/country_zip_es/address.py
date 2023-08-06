# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Address']


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    @classmethod
    def __setup__(cls):
        super(Address, cls).__setup__()
        # Remove domain as we want to be able to select all levels.
        # See: https://bugs.tryton.org/issue5563
        parent_domain = ('parent', '=', None)
        new_domain = []
        for clause in cls.subdivision.domain:
            if clause != parent_domain:
                new_domain.append(clause)
        cls.subdivision.domain = new_domain

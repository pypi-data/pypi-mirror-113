#This file is part party_search module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['Address']


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super(Address, cls).search_rec_name(name, clause)

        party_domain = ('party', clause[1], clause[2])
        if party_domain in domain:
            domain.remove(party_domain)
            domain.append(('party.name',) + tuple(clause[1:]))

        return domain + [
            ('party.contact_mechanisms.value',) + tuple(clause[1:]),
            ('party.contact_mechanisms.value_compact',) + tuple(clause[1:]),
            ]

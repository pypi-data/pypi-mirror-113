# This file is part party_lang module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Address']


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'
    full_address_lang = fields.Function(fields.Text('Full Address'),
            'get_full_address_lang')

    def get_full_address_lang(self, name):
        pool = Pool()
        Configuration = pool.get('party.configuration')
        Address = pool.get('party.address')
        context = Transaction().context

        if self.party and self.party.lang:
            language = self.party.lang.code
        else:
            config = Configuration(1)
            language = context.get('language') or config.party_lang.code

        with Transaction().set_context(language=language):
            address = Address(self)
            return address.get_full_address(name)

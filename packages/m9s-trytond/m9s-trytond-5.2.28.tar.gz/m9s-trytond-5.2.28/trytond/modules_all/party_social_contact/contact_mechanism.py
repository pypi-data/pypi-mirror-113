# This file is part of party_social_contact module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['ContactMechanism']


class ContactMechanism(metaclass=PoolMeta):
    __name__ = 'party.contact_mechanism'

    @classmethod
    def __setup__(cls):
        super(ContactMechanism, cls).__setup__()
        cls.type.selection.extend([
                ('facebook', 'Facebook'),
                ('twitter', 'Twitter'),
                ('flickr', 'Flickr'),
                ('focus', 'Focus'),
                ('google', 'Google+'),
                ('meetup', 'Meetup'),
                ('ning', 'Ning'),
                ('tuenti', 'Tuenti'),
                ('xing', 'Xing'),
                ('linkedin', 'LinkedIn'),
                ])

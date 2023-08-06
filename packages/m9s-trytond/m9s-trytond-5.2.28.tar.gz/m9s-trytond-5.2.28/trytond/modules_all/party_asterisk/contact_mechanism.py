# This file is part of party_asterisk module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['ContactMechanism']


class ContactMechanism(metaclass=PoolMeta):
    __name__ = "party.contact_mechanism"

    @classmethod
    def __setup__(cls):
        super(ContactMechanism, cls).__setup__()
        cls._buttons.update({
                'dial': {
                    'invisible': ~Eval('type').in_(['phone', 'mobile']),
                    },
                })

    @classmethod
    @ModelView.button
    def dial(cls, values):
        '''Function called by the button 'Dial' next to the 'phone' field
        in the contact_mechanism view'''
        for value in values:
            number = value.value
            Configuration = Pool().get('asterisk.configuration')
            Configuration.dial(value.party, number)

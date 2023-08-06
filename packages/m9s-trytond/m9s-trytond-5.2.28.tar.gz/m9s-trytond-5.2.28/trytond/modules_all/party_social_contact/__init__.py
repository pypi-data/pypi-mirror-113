# This file is part of party_social_contact module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import contact_mechanism


def register():
    Pool.register(
        contact_mechanism.ContactMechanism,
        module='party_social_contact', type_='model')

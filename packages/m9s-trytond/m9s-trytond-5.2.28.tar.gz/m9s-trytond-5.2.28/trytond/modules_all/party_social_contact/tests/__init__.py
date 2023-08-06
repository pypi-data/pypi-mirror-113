# This file is part of party_social_contact module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.party_social_contact.tests.test_party_social_contact import suite
except ImportError:
    from .test_party_social_contact import suite

__all__ = ['suite']

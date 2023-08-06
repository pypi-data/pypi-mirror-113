# This file is part party_identifier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.party_identifier.tests.test_party_identifier import suite
except ImportError:
    from .test_party_identifier import suite

__all__ = ['suite']

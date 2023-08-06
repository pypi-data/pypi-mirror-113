# This file is part party_tradename module for Tryton.  The COPYRIGHT file at
# the top level of this repository contains the full copyright notices and
# license terms.
try:
    from trytond.modules.party_tradename.tests.test_party_tradename import suite
except ImportError:
    from .test_party_tradename import suite

__all__ = ['suite']

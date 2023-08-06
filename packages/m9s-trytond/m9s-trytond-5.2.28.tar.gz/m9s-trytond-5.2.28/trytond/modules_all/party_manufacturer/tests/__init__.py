# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.party_manufacturer.tests.test_party_manufacturer import suite
except ImportError:
    from .test_party_manufacturer import suite

__all__ = ['suite']

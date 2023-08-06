# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.party_supplier.tests.test_party_supplier import suite
except ImportError:
    from .test_party_supplier import suite

__all__ = ['suite']

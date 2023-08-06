# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.party_customer.tests.test_party_customer import suite
except ImportError:
    from .test_party_customer import suite

__all__ = ['suite']

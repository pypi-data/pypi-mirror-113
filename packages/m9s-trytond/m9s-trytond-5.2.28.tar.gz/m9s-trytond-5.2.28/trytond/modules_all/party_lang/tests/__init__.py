# This file is part party_lang module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.party_lang.tests.test_party_lang import suite
except ImportError:
    from .test_party_lang import suite

__all__ = ['suite']

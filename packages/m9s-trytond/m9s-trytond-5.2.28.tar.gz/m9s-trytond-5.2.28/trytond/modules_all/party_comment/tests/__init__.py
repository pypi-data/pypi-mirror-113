# This file is part party_comment module for Tryton.  The COPYRIGHT file at the
# top level of this repository contains the full copyright notices and license
# terms.
try:
    from trytond.modules.party_comment.tests.test_party_comment import suite
except ImportError:
    from .test_party_comment import suite

__all__ = ['suite']

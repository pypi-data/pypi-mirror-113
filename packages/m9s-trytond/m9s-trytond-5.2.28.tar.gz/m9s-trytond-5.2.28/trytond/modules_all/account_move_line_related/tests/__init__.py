# This file is part of account_move_line_related module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.account_move_line_related.tests.test_account_move_line_related import suite
except ImportError:
    from .test_account_move_line_related import suite

__all__ = ['suite']

# This file is part company_logo module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.company_logo.tests.test_company_logo import suite
except ImportError:
    from .test_company_logo import suite

__all__ = ['suite']

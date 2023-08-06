# This file is part of sale_confirmed2quotation module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.sale_confirmed2quotation.tests.test_sale_confirmed2quotation import suite
except ImportError:
    from .test_sale_confirmed2quotation import suite

__all__ = ['suite']

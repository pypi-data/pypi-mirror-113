# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.sale_edit_inline.tests.test_sale_edit_inline import suite
except ImportError:
    from .test_sale_edit_inline import suite

__all__ = ['suite']

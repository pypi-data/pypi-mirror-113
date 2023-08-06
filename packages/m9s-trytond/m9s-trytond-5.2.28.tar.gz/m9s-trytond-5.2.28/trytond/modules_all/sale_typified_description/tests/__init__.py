# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.sale_typified_description.tests.test_sale_typified_description import suite
except ImportError:
    from .test_sale_typified_description import suite

__all__ = ['suite']

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_code_unique.tests.test_product_code_unique import suite
except ImportError:
    from .test_product_code_unique import suite

__all__ = ['suite']

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_brand.tests.test_product_brand import suite
except ImportError:
    from .test_product_brand import suite

__all__ = ['suite']

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_images.tests.test_product_images import suite
except ImportError:
    from .test_product_images import suite

__all__ = ['suite']

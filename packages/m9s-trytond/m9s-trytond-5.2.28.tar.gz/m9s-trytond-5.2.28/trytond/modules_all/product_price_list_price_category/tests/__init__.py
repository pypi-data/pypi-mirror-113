# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_price_list_price_category.tests.test_product_price_list_price_category import suite
except ImportError:
    from .test_product_price_list_price_category import suite

__all__ = ['suite']

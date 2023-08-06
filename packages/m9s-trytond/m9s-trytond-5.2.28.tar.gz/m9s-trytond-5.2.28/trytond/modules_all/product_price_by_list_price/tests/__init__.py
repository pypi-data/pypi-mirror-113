# This file is part product_price_by_list_price module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.product_price_by_list_price.tests.test_product_price_by_list_price import suite
except ImportError:
    from .test_product_price_by_list_price import suite

__all__ = ['suite']

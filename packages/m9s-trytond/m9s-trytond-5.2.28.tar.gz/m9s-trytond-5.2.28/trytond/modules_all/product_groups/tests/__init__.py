# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_groups.tests.test_product_groups import suite
except ImportError:
    from .test_product_groups import suite

__all__ = ['suite']

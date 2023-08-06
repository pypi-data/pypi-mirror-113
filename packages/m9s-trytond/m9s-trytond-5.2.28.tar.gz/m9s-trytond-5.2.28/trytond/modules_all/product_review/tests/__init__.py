# This file is part product_review module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
try:
    from trytond.modules.product_review.tests.test_product_review import suite
except ImportError:
    from .test_product_review import suite

__all__ = ['suite']

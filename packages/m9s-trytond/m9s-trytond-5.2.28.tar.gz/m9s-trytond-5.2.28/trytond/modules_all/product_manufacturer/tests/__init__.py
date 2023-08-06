# This file is part product_manufacturer module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.product_manufacturer.tests.test_product_manufacturer import suite
except ImportError:
    from .test_product_manufacturer import suite

__all__ = ['suite']

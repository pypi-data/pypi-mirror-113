# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.meta_hmi.tests.test_meta_hmi import suite
except ImportError:
    from .test_meta_hmi import suite

__all__ = ['suite']

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.production_origin.tests.test_production_origin import suite
except ImportError:
    from .test_production_origin import suite

__all__ = ['suite']

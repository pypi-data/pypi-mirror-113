# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.asset_invoice.tests.test_asset_invoice import suite
except ImportError:
    from .test_asset_invoice import suite

__all__ = ['suite']

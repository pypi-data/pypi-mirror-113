# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.asset_relationship.tests.test_asset_relationship import (
        suite)
except ImportError:
    from .test_asset_relationship import suite

__all__ = ['suite']

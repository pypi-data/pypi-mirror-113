# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

try:
    from trytond.modules.sale_channel_price_list.tests.test_sale_channel_price_list import (
        suite, create_sale_channels, create_channel_sale)
except ImportError:
    from .test_sale_channel_price_list import (
        suite, create_sale_channels, create_channel_sale)

__all__ = ['suite', 'create_sale_channels', 'create_channel_sale']

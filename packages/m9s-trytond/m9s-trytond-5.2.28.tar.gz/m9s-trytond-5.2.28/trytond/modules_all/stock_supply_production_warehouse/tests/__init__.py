# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.stock_supply_production_warehouse.tests.test_stock_supply_production_warehouse import suite
except ImportError:
    from .test_stock_supply_production_warehouse import suite

__all__ = ['suite']

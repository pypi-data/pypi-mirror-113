# This file is part sale_carrier module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.modules.company.model import (
    CompanyMultiValueMixin, CompanyValueMixin)

__all__ = ['Configuration', 'ConfigurationSaleCarrier']

sale_carrier = fields.Many2One('carrier', 'Default Carrier',
    domain=[
        ('carrier_product.salable', '=', True),
    ])


class Configuration(CompanyMultiValueMixin, metaclass=PoolMeta):
    __name__ = 'sale.configuration'
    sale_carrier = fields.MultiValue(sale_carrier)

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'sale_carrier':
            return pool.get('sale.configuration.sale_carrier')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationSaleCarrier(ModelSQL, CompanyValueMixin):
    "Sale Configuration Sale Carrier"
    __name__ = 'sale.configuration.sale_carrier'
    sale_carrier = sale_carrier

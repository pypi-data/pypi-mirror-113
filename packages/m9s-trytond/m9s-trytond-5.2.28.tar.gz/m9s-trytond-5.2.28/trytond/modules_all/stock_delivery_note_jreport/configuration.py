# This file is part stock_delivery_note_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelSQL, fields
from trytond.pool import Pool, PoolMeta
from trytond.modules.company.model import CompanyValueMixin

__all_ = ['Configuration', 'StockConfigurationCompany']


class Configuration(metaclass=PoolMeta):
    __name__ = 'stock.configuration'

    shipment_qty_decimal = fields.MultiValue(fields.Boolean(
            'Shipment Qty Decimal',
            help='Show qty with or without decimals'))

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'shipment_qty_decimal':
            return pool.get('stock.configuration.company')
        return super(Configuration, cls).multivalue_model(field)


class StockConfigurationCompany(ModelSQL, CompanyValueMixin):
    'Stock Configuration per Company'
    __name__ = 'stock.configuration.company'

    shipment_qty_decimal = fields.Boolean('Shipment Qty Decimal')

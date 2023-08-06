# This file is part jasper_reports_options module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Company']


class Company(metaclass=PoolMeta):
    __name__ = 'company.company'
    invoice_qty = fields.Boolean(
        'Invoice Qty', help='Show qty without decimals')
    sale_qty = fields.Boolean('Sale Qty', help='Show qty without decimals')
    purchase_qty = fields.Boolean(
        'Purchase Qty', help='Show qty without decimals')
    shipment_qty = fields.Boolean(
        'Shipment Qty', help='Show qty without decimals')
    invoice_header = fields.Char('Invoice Header', translate=True)
    invoice_footer = fields.Char('Invoice Footer', translate=True)
    invoice_background = fields.Char('Invoice Background', translate=True)
    show_uom = fields.Boolean('Show UoM', help='Show the UoM')
    show_origins = fields.Boolean('Show Origins', help='Show the origins')
    rgpd = fields.Char('RGPD', translate=True,
        help='Reglamento General de Proteccion de Datos (RGPD)')

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Invoice', 'InvoiceLine']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'
    shipments_origin = fields.Function(fields.One2Many('stock.shipment.out', None,
        'Shipments'), 'get_shipments_origin')
    shipments_origin_return = fields.Function(
        fields.One2Many('stock.shipment.out.return', None, 'Shipment Returns'),
        'get_shipments_origin_returns')
    shipments_origin_number = fields.Function(fields.Char('Origin Shipment Number'),
        'get_shipments_origin_number')
    shipment_origin_addresses = fields.Function(fields.Many2Many('party.address',
        None, None, 'Origin Shipment Addresses'), 'get_shipment_origin_addresses')
    shipment_origin_address = fields.Function(fields.Many2One('party.address',
        'Origin Shipment Address'), 'get_shipment_origin_address')
    sales_origin = fields.Function(fields.One2Many('sale.sale', None,
        'Sales'), 'get_sales_origin')
    sales_origin_number = fields.Function(fields.Char('Origin Sales Number'),
        'get_sales_origin_number')
    sales_origin_reference = fields.Function(fields.Char('Origin Sales Reference'),
        'get_sales_origin_reference')

    def get_shipments_origin_returns(model_name):
        "Computes the origin returns or shipments"
        def method(self, name):
            Model = Pool().get(model_name)
            shipments = set()
            for line in self.lines:
                if line.origin and line.origin.__name__ == 'sale.line':
                    for move in line.origin.moves:
                        if move.shipment and isinstance(move.shipment, Model):
                            shipments.add(move.shipment.id)
            return list(shipments)
        return method

    get_shipments_origin = get_shipments_origin_returns('stock.shipment.out')
    get_shipments_origin_returns = get_shipments_origin_returns('stock.shipment.out.return')

    def get_shipments_origin_number(self, name=None):
        numbers = []
        for shipment_origin in ['shipments_origin', 'shipments_origin_return']:
            for shipment in getattr(self, shipment_origin):
                if shipment.number:
                    numbers.append(shipment.number)
        return ', '.join(numbers)

    def get_shipment_origin_addresses(self, name=None):
        addresses = set()
        for line in self.lines:
            if line.origin and line.origin.__name__ == 'sale.line':
                if line.origin.sale and line.origin.sale.shipment_address:
                    addresses.add(line.origin.sale.shipment_address)
        return [address.id for address in addresses]

    def get_shipment_origin_address(self, name=None):
        if self.shipment_origin_addresses:
            return self.shipment_origin_addresses[0].id

    def get_sales_origin(self, name=None):
        sales = set()
        for line in self.lines:
            if line.origin and line.origin.__name__ == 'sale.line':
                if line.origin.sale:
                    sales.add(line.origin.sale)
        return [sale.id for sale in sales]

    def get_sales_origin_reference(field_name):
        "Computes the origin number or reference"
        def method(self, name):
            numbers = set()
            for line in self.lines:
                if line.origin and line.origin.__name__ == 'sale.line':
                    if line.origin.sale:
                        number = getattr(line.origin.sale, field_name)
                        if number:
                            numbers.add(number)
            return ', '.join(numbers)
        return method

    get_sales_origin_number = get_sales_origin_reference('number')
    get_sales_origin_reference = get_sales_origin_reference('reference')


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    shipments_origin = fields.Function(fields.One2Many('stock.shipment.out', None,
        'Shipments'), 'get_shipments_origin')
    shipments_origin_return = fields.Function(
        fields.One2Many('stock.shipment.out.return', None, 'Shipment Returns'),
        'get_shipments_origin_returns')
    shipments_origin_number = fields.Function(fields.Char(
        'Origin Shipment Number'), 'get_shipments_origin_fields')
    shipments_origin_effective_date = fields.Function(fields.Char(
        'Origin Shipment Effective Date'), 'get_shipments_origin_fields')
    shipment_addresses_name = fields.Function(fields.Text('Shipment Addresses'),
        'get_shipment_addresses_name')

    def get_shipments_origin_returns(model_name):
        "Computes the origin returns or shipments"
        def method(self, name):
            Model = Pool().get(model_name)
            shipments = set()
            for stock_move in self.stock_moves:
                shipment = stock_move.shipment
                if shipment and isinstance(shipment, Model):
                    shipments.add(shipment.id)
            return list(shipments)
        return method

    get_shipments_origin = get_shipments_origin_returns('stock.shipment.out')
    get_shipments_origin_returns = get_shipments_origin_returns('stock.shipment.out.return')

    def get_shipments_origin_fields(self, name=None):
        Lang = Pool().get('ir.lang')

        values = []
        for shipment_origin in ['shipments_origin', 'shipments_origin_return']:
            for shipment in getattr(self, shipment_origin):
                value = getattr(shipment, name[17:])
                if value and isinstance(value, datetime.date):
                    language = Transaction().language
                    languages = Lang.search([('code', '=', language)])
                    if not languages:
                        languages = Lang.search([('code', '=', 'en_US')])
                    language = languages[0]
                    values.append(Lang.strftime(value, language.code,
                        language.date))
                elif value:
                    values.append(value)
        return values and ', '.join(values) or ''

    @classmethod
    def get_shipment_addresses_name(cls, lines, name):
        shipment_addresses = {}
        for line in lines:
            addresses = set()
            for shipment_origin in ['shipments_origin', 'shipments_origin_return']:
                for shipment in getattr(line, shipment_origin):
                    address = []
                    if shipment.customer.name:
                        address.append(shipment.customer.name)
                    if shipment.delivery_address.street:
                        address.append(shipment.delivery_address.street)
                    if shipment.delivery_address.zip:
                        address.append(shipment.delivery_address.zip)
                    if shipment.delivery_address.subdivision:
                        address.append(shipment.delivery_address.subdivision.name)
                    addresses.add(', '.join(address))
            shipment_addresses[line.id] = '\n'.join(addresses) if addresses else None
        return shipment_addresses

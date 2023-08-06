# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import datetime
from decimal import Decimal
from dateutil.relativedelta import relativedelta
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.modules.company.tests import create_company, set_company
from trytond.transaction import Transaction


class ProductTemplateFormQuantityTestCase(ModuleTestCase):
    'Test Product Template Form Quantity module'
    module = 'product_template_form_quantity'

    @with_transaction()
    def test_quantiy(self):
        'Test quantity'
        pool = Pool()
        Configuration = pool.get('stock.configuration')
        Move = pool.get('stock.move')
        Location = pool.get('stock.location')
        Template = pool.get('product.template')
        Uom = pool.get('product.uom')

        company = create_company()
        currency = company.currency
        with set_company(company):
            today = datetime.date.today()

            u, = Uom.search([('name', '=', 'Unit')])
            template, = Template.create([{
                        'name': 'Product',
                        'default_uom': u.id,
                        'list_price': Decimal(0),
                        'products': [('create', [{}])],
                        }])
            product, = template.products

            input_location, output_location, storage_location  = Location.create([{
                        'name': 'Input 2',
                        'type': 'storage',
                        }, {
                        'name': 'Output 2',
                        'type': 'storage',
                        }, {
                        'name': 'Storage 2',
                        'type': 'storage',
                        }])

            Location.create([{
                        'name': 'Warehouse2',
                        'type': 'warehouse',
                        'input_location': input_location,
                        'output_location': output_location,
                        'storage_location': storage_location,
                        }])

            warehouse1, warehouse2 = Location.search([
                        ('type', '=', 'warehouse'),
                        ])
            lost_found, = Location.search([('type', '=', 'lost_found')])

            moves = Move.create([{
                        'product': product.id,
                        'uom': u.id,
                        'quantity': 5,
                        'from_location': lost_found.id,
                        'to_location': warehouse1.storage_location.id,
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }, {
                        'product': product.id,
                        'uom': u.id,
                        'quantity': 10,
                        'from_location': lost_found.id,
                        'to_location': warehouse2.storage_location.id,
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }])
            Move.do(moves)

            with Transaction().set_context(locations=[
                        warehouse1.storage_location.id,
                        warehouse2.storage_location.id,
                        ]):
                template = Template(product.template.id)
            self.assertEqual(template.quantity, Decimal('15.0'))

            moves = Move.create([{
                        'product': product.id,
                        'uom': u.id,
                        'quantity': 5,
                        'from_location': lost_found.id,
                        'to_location': warehouse1.storage_location.id,
                        'planned_date': today + relativedelta(days=5),
                        'effective_date': today + relativedelta(days=5),
                        'company': company.id,
                        'unit_price': Decimal('1'),
                        'currency': currency.id,
                        }])
            Move.do(moves)

            configuration = Configuration(1)
            configuration.warehouse = warehouse1
            configuration.lag_days = 10
            configuration.save()

            template = Template(product.template.id)
            # not sum 5 + 5 (total 10)
            # because effective date last move is today + 5
            self.assertEqual(template.quantity, Decimal('5.0'))
            self.assertEqual(template.forecast_quantity, Decimal('10.0'))


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        ProductTemplateFormQuantityTestCase))
    return suite

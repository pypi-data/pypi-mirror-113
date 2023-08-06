# This file is part of the stock_origin_sale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from decimal import Decimal
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account.tests import create_chart


def create_payment_term():
    PaymentTerm = Pool().get('account.invoice.payment_term')

    term, = PaymentTerm.create([{
                'name': '0 days',
                'lines': [
                    ('create', [{
                                'sequence': 0,
                                'type': 'remainder',
                                'relativedeltas': [('create', [{},
                                            ]),
                                    ],
                                }])]
                }])
    return term


class StockOriginSaleTestCase(ModuleTestCase):
    'Test Stock Origin Sale module'
    module = 'stock_origin_sale'

    @with_transaction()
    def test_sale(self):
        "Test Sale"
        pool = Pool()
        Account = pool.get('account.account')
        Party = pool.get('party.party')
        Uom = pool.get('product.uom')
        Template = pool.get('product.template')
        Category = pool.get('product.category')
        Sale = pool.get('sale.sale')
        SaleLine = pool.get('sale.line')
        ShipmentOut = pool.get('stock.shipment.out')
        ShipmentOutReturn = pool.get('stock.shipment.out.return')

        company = create_company()
        with set_company(company):
            create_chart(company, tax=True)
            create_payment_term()
            account_expense, = Account.search([
                    ('type.expense', '=', True),
                    ], limit=1)
            account_revenue, = Account.search([
                    ('type.revenue', '=', True),
                    ], limit=1)

            # party
            party1 = Party()
            for key, value in Party.default_get(Party._fields.keys(),
                    with_rec_name=False).items():
                if value is not None:
                    setattr(party1, key, value)
            party1.save()

            # category
            account_category = Category()
            account_category.name = 'Account Category'
            account_category.accounting = True
            account_category.account_expense = account_expense
            account_category.account_revenue = account_revenue
            account_category.save()

            # product
            unit, = Uom.search([('name', '=', 'Unit')])
            template1 = Template()
            for key, value in Template.default_get(Template._fields.keys(),
                    with_rec_name=False).items():
                if value is not None:
                    setattr(template1, key, value)
            template1.name = 'Product 1'
            template1.list_price = Decimal(12)
            template1.cost_price = Decimal(10)
            template1.default_uom = unit
            template1.salable = True
            template1.purchasable = True
            template1.on_change_default_uom()
            template1.account_category = account_category
            template1.save()
            product1, = template1.products

            # sale
            sale = Sale()
            for key, value in Sale.default_get(Sale._fields.keys(),
                    with_rec_name=False).items():
                if value is not None:
                    setattr(sale, key, value)
            sale.party = party1
            sale.reference = 'REF1'
            sale.on_change_party()

            for qty in [2.0, -1.0]:
                sline = SaleLine()
                sline.sale = sale
                for key, value in SaleLine.default_get(SaleLine._fields.keys(),
                        with_rec_name=False).items():
                    if value is not None:
                        setattr(sline, key, value)
                sline.product = product1
                sline.quantity = qty
                sline.on_change_product()
                sline.save()

            # quote and confirm sale
            Sale.quote([sale])
            Sale.confirm([sale])
            Sale.process([sale])
            self.assertEqual(sale.number, '1')
            self.assertEqual(len(sale.shipments), 1)

            shipment, = sale.shipments
            self.assertEqual(shipment.origin.number, '1')
            self.assertEqual(shipment.origin_cache.number, '1')
            self.assertEqual(shipment.origin_info, 'Sale,1')
            self.assertEqual(shipment.origin_number, '1')
            self.assertEqual(shipment.origin_reference, 'REF1')

            shipment_out, = ShipmentOut.search([
                ('origin_number', '=', '1'),
                ])
            self.assertEqual(shipment_out.origin_number, '1')

            shipment_out_return, = ShipmentOutReturn.search([
                ('origin_number', '=', '1'),
                ])
            self.assertEqual(shipment_out_return.origin_number, '1')


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        StockOriginSaleTestCase))
    return suite

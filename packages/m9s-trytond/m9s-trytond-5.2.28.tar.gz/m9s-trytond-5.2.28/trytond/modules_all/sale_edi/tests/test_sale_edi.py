# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import os
import shutil
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account.tests import create_chart, get_fiscalyear
from trytond.modules.account_invoice.tests import set_invoice_sequences
from decimal import Decimal


TEST_FILES_DIR = os.path.abspath(
    'trytond/trytond/modules/sale_edi/tests/data/tmp')
TEST_FILES_EXTENSION = '.txt'


class TestCase(ModuleTestCase):
    'Test module'
    module = 'sale_edi'

    def create_fiscalyear_and_chart(self, company=None, fiscalyear=None,
            chart=True):
        'Test fiscalyear'
        pool = Pool()
        FiscalYear = pool.get('account.fiscalyear')
        if not company:
            company = create_company()
        with set_company(company):
            if chart:
                create_chart(company)
            if not fiscalyear:
                fiscalyear = set_invoice_sequences(get_fiscalyear(company))
                fiscalyear.save()
                FiscalYear.create_period([fiscalyear])
                self.assertEqual(len(fiscalyear.periods), 12)
            return fiscalyear

    def get_accounts(self, company):
        pool = Pool()
        Account = pool.get('account.account')
        accounts = {}
        accounts['receivable'] = Account.search([
            ('type.receivable', '=', True),
            ('company', '=', company.id),
            ])[0]
        accounts['payable'] = Account.search([
            ('type.payable', '=', True),
            ('company', '=', company.id),
            ])[0]

        accounts['revenue'] = Account.search([
            ('type.revenue', '=', True),
            ('company', '=', company.id),
            ])[0]
        accounts['expense'] = Account.search([
            ('type.expense', '=', True),
            ('company', '=', company.id),
            ])[0]

        root, = Account.search([
                ('parent', '=', None),
                ('company', '=', company.id),
                ], limit=1)
        accounts['root'] = root
        if not accounts['revenue'].code:
            accounts['revenue'].parent = root
            accounts['revenue'].code = '7'
            accounts['revenue'].save()
        if not accounts['receivable'].code:
            accounts['receivable'].parent = root
            accounts['receivable'].code = '43'
            accounts['receivable'].save()
        if not accounts['expense'].code:
            accounts['expense'].parent = root
            accounts['expense'].code = '6'
            accounts['expense'].save()
        if not accounts['payable'].code:
            accounts['payable'].parent = root
            accounts['payable'].code = '41'
            accounts['payable'].save()
        cash, = Account.search([
                ('name', '=', 'Main Cash'),
                ('company', '=', company.id),
                ], limit=1)
        accounts['cash'] = cash
        tax, = Account.search([
                ('name', '=', 'Main Tax'),
                ('company', '=', company.id),
                ], limit=1)
        accounts['tax'] = tax
        views = Account.search([
                ('name', '=', 'View'),
                ('company', '=', company.id),
                ], limit=1)
        if views:
            view, = views
        else:
            with set_company(company):
                view, = Account.create([{
                            'name': 'View',
                            'code': '1',
                            'parent': root.id,
                            }])
        accounts['view'] = view
        return accounts

    def create_parties(self, company):
        pool = Pool()
        Party = pool.get('party.party')
        with set_company(company):
            return Party.create([{
                        'name': 'customer1',
                        'addresses': [('create', [{}])],
                    }, {
                        'name': 'customer2',
                        'addresses': [('create', [{}])],
                    }, {
                        'name': 'supplier1',
                        'addresses': [('create', [{}])],
                    }, {
                        'name': 'supplier2',
                        'addresses': [('create', [{'active': False}])],
                        'active': False,
                    }])

    def get_parties(self):
        pool = Pool()
        Party = pool.get('party.party')
        customer1, = Party.search([
                ('name', '=', 'customer1'),
                ], limit=1)
        customer2, = Party.search([
                ('name', '=', 'customer2'),
                ], limit=1)
        supplier1, = Party.search([
                ('name', '=', 'supplier1'),
                ], limit=1)
        with Transaction().set_context(active_test=False):
            supplier2, = Party.search([
                    ('name', '=', 'supplier2'),
                    ], limit=1)
        return customer1, customer2, supplier1, supplier2

    def create_payment_term(self):
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

    @with_transaction()
    def test_get_sales_from_edi_file(self):
        pool = Pool()
        Party = pool.get('party.party')
        ProductUom = pool.get('product.uom')
        ProductTemplate = pool.get('product.template')
        PartyIdentifier = pool.get('party.identifier')
        Product = pool.get('product.product')
        ProductCategory = pool.get('product.category')
        Tax = pool.get('account.tax')
        Sale = pool.get('sale.sale')
        SaleConfig = pool.get('sale.configuration')

        if not os.path.exists(TEST_FILES_DIR):
            os.mkdir(TEST_FILES_DIR)
        test_fname = ('trytond/trytond/modules/sale_edi/tests/data/order' +
            TEST_FILES_EXTENSION)
        shutil.copy(test_fname, TEST_FILES_DIR)

        company = create_company()
        with set_company(company):
            self.create_fiscalyear_and_chart(company, None,
                True)
            # Create some parties
            customer1, customer2, supplier1, supplier2 = self.create_parties(
                company)
            accounts = self.get_accounts(company)
            expense = accounts.get('expense')
            revenue = accounts.get('revenue')
            rate = Decimal('.10')
            tax = Tax()
            tax.name = 'Tax %s' % rate
            tax.description = tax.name
            tax.type = 'percentage'
            tax.rate = rate
            tax.invoice_account = accounts.get('tax')
            tax.credit_note_account = accounts.get('tax')
            term = self.create_payment_term()
            customer, = Party.search([
                    ('name', '=', 'customer1'),
                    ], limit=1)
            customer.customer_payment_term = term
            customer.save()
            identifier = PartyIdentifier()
            identifier.type = 'edi'
            identifier.code = 'PUNTO_VENTA'
            identifier.party = customer
            identifier.save()
            address, = customer.addresses
            address.edi_ean = 'PUNTO_VENTA'
            address.save()
            sale_cfg = SaleConfig(1)
            sale_cfg.edi_source_path = os.path.abspath(TEST_FILES_DIR)
            sale_cfg.save()
            unit, = ProductUom.search([('name', '=', 'Unit')], limit=1)
            category = ProductCategory(name='test account used',
                account_expense=expense, accounting=True)
            category.save()
            template = ProductTemplate()
            template.name = 'product'
            template.default_uom = unit
            template.type = 'goods'
            template.account_category = category
            template.purchasable = True
            template.salable = True
            template.list_price = Decimal('10')
            template.cost_price_method = 'fixed'
            template.account_expense = expense
            template.account_revenue = revenue
            template.sale_uom = unit
            template.save()
            product = Product()
            product.template = template
            product.cost_price = Decimal('5')
            product.code = '67310'
            product.save()
            sales = Sale.get_sales_from_edi_files()
            self.assertTrue(sales)
            sale = sales[0]
            self.assertEqual(sale.payment_term, term)
            self.assertEqual(sale.shipment_party, customer)
            self.assertEqual(sale.party, customer)
            self.assertTrue(sale.lines)
            line = sale.lines[0]
            self.assertEqual(line.product.code, product.code)
            os.rmdir(TEST_FILES_DIR)


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(TestCase))
    return suite

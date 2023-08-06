# This file is part stock_traceability_report module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
import unittest
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.tests.test_tryton import suite as test_suite
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.modules.company.tests import create_company, set_company
from trytond.modules.html_report.engine import DualRecord


class StockTraceabilityReportTestCase(ModuleTestCase):
    'Test Stock Traceability Report module'
    module = 'stock_traceability_report'

    @with_transaction()
    def test_tracebility_report(self):
        'Test Tracebility report'
        pool = Pool()
        Uom = pool.get('product.uom')
        Template = pool.get('product.template')
        Product = pool.get('product.product')
        Location = pool.get('stock.location')
        Move = pool.get('stock.move')
        PrintStockTraceabilityReport = pool.get('stock.traceability.report', type='report')
        PrintStockTraceability = pool.get('stock.print_traceability', type='wizard')

        unit, = Uom.search([('name', '=', 'Unit')])
        template, = Template.create([{
                    'name': 'Test Move',
                    'type': 'goods',
                    'list_price': Decimal(1),
                    'default_uom': unit.id,
                    }])
        product, = Product.create([{
                    'template': template.id,
                    }])
        supplier, = Location.search([('code', '=', 'SUP')])
        storage, = Location.search([('code', '=', 'STO')])

        company = create_company()
        currency = company.currency
        with set_company(company):
            for quantity in [10, 100, 1, 35]:
                move, = Move.create([{
                            'product': product.id,
                            'uom': unit.id,
                            'quantity': quantity,
                            'from_location': supplier.id,
                            'to_location': storage.id,
                            'company': company.id,
                            'unit_price': Decimal('1'),
                            'currency': currency.id,
                            }])
                Move.do([move])

            session_id, _, _ = PrintStockTraceability.create()
            print_traceability = PrintStockTraceability(session_id)
            print_traceability.start.warehouse = storage.warehouse
            print_traceability.start.from_date = None
            print_traceability.start.to_date = None
            with Transaction().set_context(active_ids=[product.id], active_model='product.product'):
                _, data = print_traceability.do_print_(None)
                records, parameters = PrintStockTraceabilityReport.prepare(data)
                record, = records
                self.assertEqual(type(record['product']), DualRecord)
                self.assertEqual(record['supplier_incommings_total'], 146)
                self.assertEqual(len(record['supplier_incommings']), 4)

def suite():
    suite = test_suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            StockTraceabilityReportTestCase))
    return suite

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool


class BankingImportRuleInformation(metaclass=PoolMeta):
    __name__ = 'banking.import.rule.information'

    def _get_invoice(self, origin, keywords):
        pool = Pool()
        Sale = pool.get('sale.sale')

        super()._get_invoice(self, origin, keywords)
        # Customers could also put the sale number as reference
        if keywords.get('invoice'):
            sales = Sale.search([('rec_name', '=', keywords['invoice'])])
            if len(sales) == 1:
                sale, = sales
                return sale.invoices[0]
        # PayPal parsing of Sale ID
        if keywords.get('sale'):
            sales = Sale.search([('id', '=', int(keywords['sale']))])
            if len(sales) == 1:
                sale, = sales
                return sale.invoices[0]

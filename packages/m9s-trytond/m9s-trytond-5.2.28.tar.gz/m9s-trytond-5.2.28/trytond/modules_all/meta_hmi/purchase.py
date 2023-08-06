# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    @staticmethod
    def default_quantity():
        return 1

    @fields.depends('product', 'description', '_parent_purchase.party')
    def on_change_product(self):
        '''
        purchase
          - use the name of the product instead of rec_name
          - append the supplier number to the product description
        '''
        pool = Pool()
        Product = pool.get('product.product')
        ProductSupplier = pool.get('purchase.product_supplier')

        super(PurchaseLine, self).on_change_product()
        if not self.product:
            return

        context = {}
        party = None
        if self.purchase and self.purchase.party:
            party = self.purchase.party
            if party.lang:
                context['language'] = party.lang.code
        if not self.description:
            product_supplier = ProductSupplier.search([
                    ('party', '=', self.purchase.party.id),
                    ('product', '=', self.product.id),
                    ])
            with Transaction().set_context(context):
                self.description = Product(self.product.id).name
            if product_supplier and product_supplier[0].code:
                self.description += ' [%s]' % (product_supplier[0].code,)

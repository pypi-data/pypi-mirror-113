# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['PurchaseLine']


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    supplier_product_code = fields.Function(
        fields.Char('Supplier Product Code'),
        'on_change_with_supplier_product_code')

    @fields.depends('product', '_parent_purchase.party', 'purchase')
    def on_change_with_supplier_product_code(self, name=None):
        if self.purchase and self.product:
            for psupplier in self.product.product_suppliers:
                if psupplier.party == self.purchase.party:
                    return psupplier.code

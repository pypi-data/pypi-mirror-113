# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import math

from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Bool
from trytond.exceptions import UserError
from trytond.i18n import gettext
from trytond.transaction import Transaction

STATES = {
    'invisible': Bool(~Eval('kit')),
    }
DEPENDS = ['kit']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    @classmethod
    def validate(cls, templates):
        super(Template, cls).validate(templates)
        for template in templates:
            template.check_type_and_products_stock_depends()

    def check_type_and_products_stock_depends(self):
        if not (self.consumable or self.type == 'service'):
            for product in self.products:
                product.check_stock_depends_and_product_type()


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'
    stock_depends_on_kit_components = fields.Boolean('Stock Depends on '
            'Components', states=STATES, depends=DEPENDS,
            help='Indicates whether the stock of the current kit should '
                  'depend on its components or not.')

    @staticmethod
    def default_stock_depends_on_kit_components():
        return False

    @classmethod
    def get_quantity(cls, products, name):
        quantities = super(Product, cls).get_quantity(products, name)

        def get_quantity_kit(product, quantities):
            pack_stock = 0.0
            for subproduct in product.kit_lines:
                sub_qty = subproduct.quantity
                sub_stock = cls.get_quantity(
                        [subproduct.product], name)[subproduct.product.id]
                # If any component is missing, the kit is just not available
                if sub_stock <= 0:
                    return 0.0
                sub_stock = math.floor(sub_stock / sub_qty)
                if not pack_stock:
                    pack_stock = sub_stock
                else:
                    pack_stock = min(pack_stock, sub_stock)
            return pack_stock

        kits = [p for p in products if p.kit]
        while kits:
            kit = kits.pop(0)
            if kit.stock_depends_on_kit_components and kit.kit_lines:
                quantities[kit.id] = get_quantity_kit(kit, quantities)
        return quantities

    @classmethod
    def validate(cls, products):
        super(Product, cls).validate(products)
        for product in products:
            product.check_stock_depends_and_product_type()

    def check_stock_depends_and_product_type(self):
        if (self.stock_depends_on_kit_components
                and not (self.consumable or self.type == 'service')):
            raise UserError(gettext(
                'stock_kit.invalid_stock_depends_and_type',
                product=self.rec_name))

    @classmethod
    def products_by_location(cls, location_ids,
            with_childs=False, grouping=('product',), grouping_filter=None):
        """
        For kits configured as stock_depends_on_kit_components:
            Compute only for storage location the quantities of the components
            and return the minimal quantity of the least one.
        """
        pool = Pool()
        Location = pool.get('stock.location')

        product_id = Transaction().context.get('product')
        calculate_components = False
        if product_id:
            product, = cls.browse([product_id])
            if product.kit and product.stock_depends_on_kit_components:
                calculate_components = True
        if not product_id or not calculate_components:
            return super().products_by_location(location_ids,
                with_childs=with_childs, grouping=grouping,
                grouping_filter=grouping_filter)

        # Since this is a virtual number that applies only for the current
        # availability of a kit we consider only the storage location and
        # take that number also for the warehouse
        quantities = {}
        warehouses = Location.search([
                    ('type', '=', 'warehouse'),
                    ], order=[('left', 'DESC')])
        if warehouses:
            warehouse = warehouses[0]
        else:
            return quantities

        storage_id = warehouse.storage_location.id
        kit_stock = 0.0
        for line in product.kit_lines:
            component_id = line.product.id
            with Transaction().set_context(product=component_id):
                comp_stock = cls.products_by_location([storage_id],
                    with_childs=with_childs, grouping=grouping,
                    grouping_filter=([component_id],))
                if comp_stock:
                    qty = next(iter(comp_stock.values()))
                    if not kit_stock:
                        kit_stock = qty
                    else:
                        kit_stock = min(kit_stock, qty)

        if kit_stock:
            quantities = {
                (storage_id, product_id): kit_stock,
                (warehouse.id, product_id): kit_stock
                }
        return quantities

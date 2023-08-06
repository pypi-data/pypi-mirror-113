# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import Workflow, ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool, Id
from trytond.wizard import Wizard, StateTransition

from trytond.modules.shipping.mixin import ShipmentCarrierMixin \
    as ShipmentMixin


class ShipmentCarrierMixin(ShipmentMixin):

    def get_weight_uom(self, name):
        """
        Returns weight uom for the shipment
        """
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_kilogram')


class Package(metaclass=PoolMeta):
    __name__ = "stock.package"

    #@classmethod
    #def search_rec_name(cls, name, clause):
    #    domain = super(Package, cls).search_rec_name(name, clause)
    #    return ['OR', domain,
    #        ('shipping_reference',) + tuple(clause[:1]),
    #        ]

    @staticmethod
    def default_distance_unit():
        '''
        shipping
         - set a custom distance unit for EU
        '''
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_centimeter')

    @staticmethod
    def default_override_weight_uom():
        '''
        shipping
         - set a custom uom unit for EU
        '''
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_gram')

    # stock_package_shipping *and* shipping/mixin.py both provide
    # function field weight with getter get_weight.
    # We go for now with stock_package_shipping and use this
    # monkey patch.
    def _get_weight(self, name):
        pool = Pool()
        UoM = pool.get('product.uom')
        UoMCategory = pool.get('product.uom.category')
        ModelData = pool.get('ir.model.data')

        weight_category = UoMCategory(
            ModelData.get_id('product', 'uom_cat_weight'))
        kg = UoM(ModelData.get_id('product', 'uom_kilogram'))

        weight = 0
        for move in self.moves:
            # Use first the weight from product_measurements as it could
            # include some handling weight
            if move.product.weight is not None:
                weight += UoM.compute_qty(
                    move.product.weight_uom,
                    move.internal_quantity * move.product.weight,
                    kg, round=False)
            elif move.product.default_uom.category == weight_category:
                weight += UoM.compute_qty(
                    move.product.default_uom,
                    move.internal_quantity,
                    kg, round=False)
            else:
                weight = None
                break
        return weight

    def get_weight(self, name):
        # stock_package_shipping converts hard coded to kg
        # We can not super, see above
        weight = self._get_weight(name)
        # We add for now 100g package weight for Tara until
        # stock_shipment_measurements is backported or can be used
        # #3792
        if weight is None:
            weight = 0
        # Tara
        weight += 0.1
        # Minimum weight for GLS package
        if weight < 1.0:
            weight = 1.0
        return weight


class CreateSaleShipping(metaclass=PoolMeta):
    __name__ = 'stock.shipment.sale.create_shipping'

    def get_package(self):
        # Put all not yet packaged moves into the default package
        # #3791
        package = super(CreateSaleShipping, self).get_package()

        shipment = self.start.shipment
        packed_moves = set()
        for package_ in shipment.packages:
            for move in package_.moves:
                packed_moves.add(move)
        outgoing_moves = set(shipment.outgoing_moves)
        moves_to_pack = outgoing_moves - packed_moves
        if moves_to_pack:
            package.moves = list(moves_to_pack)
        return package


class CreateSaleShippingStart(metaclass=PoolMeta):
    __name__ = 'stock.shipment.sale.create_shipping.start'

    @classmethod
    def __setup__(cls):
        super(CreateSaleShippingStart, cls).__setup__()
        # Preuninger wants to create labels for sales order quotations (#3632).
        cls.shipment.domain = [
            ('state', 'in', ['waiting', 'packed', 'done']),
            ]

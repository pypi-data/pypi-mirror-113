# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView
from trytond.pool import PoolMeta

__all__ = ['ShipmentOut']


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    @classmethod
    def __setup__(cls):
        super(ShipmentOut, cls).__setup__()
        assign_wizard = cls._buttons['assign_wizard']
        cls._buttons.update({
                'assign_wizard': {
                    'invisible': True,
                    },
                'assign_try_button': assign_wizard,
                })

    @classmethod
    @ModelView.button
    def assign_try_button(cls, shipments):
        cls.assign_try(shipments)
        # Don't return anything otherwise and action is openend on the client
        return

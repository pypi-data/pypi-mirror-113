# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['ShipmentInReturn']


class ShipmentInReturn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.in.return'

    @classmethod
    def __setup__(cls):
        super(ShipmentInReturn, cls).__setup__()
        new_domain = []
        for clause in cls.moves.domain:
            if isinstance(clause, (list, tuple)):
                if clause[0] == 'from_location':
                    new_clause = [
                        ('from_location', 'child_of', Eval('from_location'),
                        'parent')]
                else:
                    new_clause = clause
            else:
                new_clause = clause
            new_domain.append(new_clause)
        cls.moves.domain = new_domain
        readonly = cls.moves.states.get('readonly')
        cls.moves.states['readonly'] = readonly & (Eval('state') != 'waiting')

    @classmethod
    def assign_try(cls, shipments):
        pool = Pool()
        Move = pool.get('stock.move')
        success = super(ShipmentInReturn, cls).assign_try(shipments)
        if not success:
            # Try to assign with childs
            if Move.assign_try([m for s in shipments for m in s.moves]):
                cls.assign(shipments)
                return True
            else:
                return False
        return success

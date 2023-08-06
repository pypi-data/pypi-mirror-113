# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool


class OrderPoint(metaclass=PoolMeta):
    __name__ = "stock.order_point"

    @staticmethod
    def default_warehouse_location():
        '''
        stock_supply
         - try to preset the warehouse
        '''
        Location = Pool().get('stock.location')
        warehouses = Location.search([
                ('type', '=', 'warehouse'),
                ])
        if len(warehouses) == 1:
            return warehouses[0].id

    # 5.2 seem both fixed
    #@classmethod
    #def search_rec_name(cls, name, clause):
    #    '''
    #    stock_supply
    #     - we override completely, because there is no need to search for
    #       template names (as in stock_supply)(#2679).
    #    '''
    #    res = []
    #    names = clause[2].split('@', 1)
    #    res.append(('product.name', clause[1], names[0]))
    #    if len(names) != 1 and names[1]:
    #        res.append(('location', clause[1], names[1]))
    #    return res

    #@classmethod
    #def search_location(cls, name, domain=None):
    #    '''
    #    stock_supply
    #     - Fix for #2680 (upstream bug)
    #    '''
    #    ids = []
    #    for type, field in cls._type2field().items():
    #        args = [('type', '=', type)]
    #        args.append((field, domain[1], domain[2]))
    #        ids.extend([o.id for o in cls.search(args)])
    #    return [('id', 'in', ids)]

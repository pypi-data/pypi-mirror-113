# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.transaction import Transaction


class PurchaseRequest(metaclass=PoolMeta):
    __name__ = 'purchase.request'

    @classmethod
    def search_rec_name(cls, name, clause):
        '''
        stock_supply
         - override completely, because there is no need to search for
           template names (#2679).
         - search also for the party rec_name
        '''
        res = []
        names = clause[2].split('@', 1)
        res.append(['OR',
                ('product.name', clause[1], names[0]),
                ('party.rec_name', clause[1], names[0])
                ])
        if len(names) != 1 and names[1]:
            res.append(('warehouse', clause[1], names[1]))
        return ['OR', res,
            ('description',) + tuple(clause[1:]),
            ]

    @classmethod
    def generate_requests(cls, products=None, warehouses=None):
        '''
        stock_supply
          - we also want assigned products to be considered in purchase
            requests (#2877)
            This should usually be a patch in the context for pbl,
            but we keep it simple and write the general context
        '''
        with Transaction().set_context(stock_assign=True):
            super(PurchaseRequest, cls).generate_requests(products=products,
                warehouses=warehouses)

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['Move']


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'

    purchase_date = fields.Function(fields.Date(
        'Purchase Date'), 'get_purchase_relation',
        searcher='search_purchase_planned_date')
    purchase_planned_date = fields.Function(fields.Date(
        'Purchase Planned Date'), 'get_purchase_relation',
        searcher='search_purchase_planned_date')
    warehouse_supplier = fields.Function(fields.Many2One('stock.location',
        'Warehouse', domain=[('type', '=', 'warehouse')]),
        'get_purchase_relation', searcher='search_warehouse_supplier')
    shipment_supplier = fields.Function(fields.Many2One('party.party', 'Supplier'),
        'get_purchase_relation', searcher='search_shipment_supplier')

    @classmethod
    def get_purchase_relation(cls, moves, names):
        res = {n: {m.id: None for m in moves} for n in names}

        for name in names:
            for move in moves:
                if name == 'purchase_date':
                    res[name][move.id] = (move.purchase.purchase_date
                        if move.purchase else None)
                if name == 'purchase_planned_date':
                    res[name][move.id] = ((move.origin.delivery_date_store
                        or (move.origin.purchase
                        and move.origin.purchase.delivery_date)) if (move.origin
                        and move.origin.__name__ == 'purchase.line') else move.planned_date)
                elif name == 'warehouse_supplier':
                    if move.shipment and move.shipment.__name__ == 'stock.shipment.in':
                        res[name][move.id] = (move.to_location.warehouse.id
                            if move.to_location.warehouse else None)
                    elif move.shipment and move.shipment.__name__ == 'stock.shipment.in.return':
                        res[name][move.id] = (move.from_location.warehouse.id
                            if move.from_location.warehouse else None)
                    else:
                        res[name][move.id] = (move.to_location.warehouse.id
                            if move.to_location.warehouse else None)
                elif name == 'shipment_supplier':
                    if move.shipment:
                        res[name][move.id] = move.shipment.supplier.id
                    elif move.purchase:
                        res[name][move.id] = move.purchase.party.id
        return res

    @classmethod
    def search_purchase_planned_date(cls, name, clause):
        # return [('purchase.delivery_date',) + tuple(clause[1:])]
        return ['OR',
            ('purchase.delivery_date',) + tuple(clause[1:]),
            ('origin.delivery_date_store',) + tuple(clause[1:3])
                + ('purchase.line',) + tuple(clause[3:])]

    @classmethod
    def search_warehouse_supplier(cls, name, clause):
        return ['OR',
            ('to_location.warehouse',) + tuple(clause[1:]),
            ('from_location.warehouse',) + tuple(clause[1:])]

    @classmethod
    def search_shipment_supplier(cls, name, clause):
        return ['OR',
            ('shipment.supplier' + clause[0].lstrip(name),)
                + tuple(clause[1:3]) + ('stock.shipment.in.return',)
                + tuple(clause[3:]),
            ('shipment.supplier' + clause[0].lstrip(name),)
                + tuple(clause[1:3]) + ('stock.shipment.in',)
                + tuple(clause[3:]),
            ('purchase.party',) + tuple(clause[1:]),
            ]

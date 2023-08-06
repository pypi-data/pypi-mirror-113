# This file is part stock_lot_by_location module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pyson import PYSONEncoder
from trytond.pool import Pool
from trytond.transaction import Transaction
from trytond.wizard import Wizard, StateAction

_all__ = ['LotByLocations']


class LotByLocations(Wizard):
    'Lot by Locations'
    __name__ = 'stock.lot.by_locations'
    start = StateAction('stock_lot_by_location.act_lots_by_locations')

    def do_start(self, action):
        pool = Pool()
        Lot = pool.get('stock.lot')

        lot_id = Transaction().context['active_id']
        lot = Lot(lot_id)

        context = {}
        context['product'] = lot.product.id
        context['lot'] = lot_id

        action['name'] += ' - %s (%s)' % (lot.rec_name,
            lot.product.default_uom.rec_name)
        action['pyson_context'] = PYSONEncoder().encode(context)
        return action, {}

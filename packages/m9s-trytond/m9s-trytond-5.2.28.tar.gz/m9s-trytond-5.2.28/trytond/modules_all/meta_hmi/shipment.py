# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.model import ModelView, Workflow
from trytond.transaction import Transaction
from trytond.tools import grouped_slice


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    send_mail_on_shipping = fields.Function(fields.Char(
            'Send mail on shipping'), 'get_shipping_information')
    mail_cc = fields.Function(fields.Char(
            'Mail CC'), 'get_shipping_information')
    delivery_full_name = fields.Function(fields.Char(
            'Delivery Full Name'), 'get_shipping_information')

    def get_rec_name(self, name):
        field_names = [
            self.number,
            self.customer.rec_name,
            ]
        return ' - '.join(filter(None, field_names))

    @classmethod
    def get_shipping_information(cls, shipments, name):
        '''
        E.g. for use
        - in the evaluation of trigger conditions in email templates
          - Check for state 'done'
          - Do not send mail for self pick up
          - Send pick_up mail if no carrier or carrier is our own company
          - Else send delivery mail
        - in the evaluation of genshi statements in email templates
        '''
        Sale = Pool().get('sale.sale')

        res = {s.id: '' for s in shipments}
        shipments_done = [s for s in shipments if s.state == 'done']
        for shipment in shipments_done:
            if name == 'send_mail_on_shipping':
                res[shipment.id] = 'send'
            if shipment.origins:
                origin = shipment.origins.split(',')[0]
                # Get the number from the rec_name, search for rec_name doesn't
                # work
                number = origin.split(' - ')[1]
                sales = Sale.search([
                        ('number', '=', number),
                        ])
                if sales:
                    sale = sales[0]
                    if name == 'send_mail_on_shipping':
                        if sale.self_pick_up:
                            res[shipment.id] = 'self_pick_up'
                        elif (sale.carrier
                                and (sale.carrier.party.id
                                    == shipment.company.party.id)):
                            res[shipment.id] = 'pick_up'
                    if name == 'mail_cc':
                        delivery_mail = shipment.customer.email
                        order_mail = sale.party.email
                        if delivery_mail != order_mail:
                            res[shipment.id] = order_mail
                    if name == 'delivery_full_name':
                        res[shipment.id] = shipment.customer.full_name
                        if shipment.customer.id != sale.party.id:
                            res[shipment.id] = sale.party.full_name
            return res

    def get_weight_uom(self, name):
        '''
        shipping
            - set a custom weight unit for EU
        '''
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_gram')

    def _get_carrier_context(self):
        '''
        sale_shipment_cost
          - Provide the sale in the context if it can be found on the moves
            Used in .carrier/get_sale_price for carrier calculation
        '''
        res = super(ShipmentOut, self)._get_carrier_context()
        if self.id:
            # Re-browse to avoid key error for moves
            shipment, = self.__class__.browse([self.id])
            for move in shipment.moves:
                if move.sale:
                    res['sale'] = move.sale.id
                    break
        return res


class ShipmentIn(metaclass=PoolMeta):
    __name__ = 'stock.shipment.in'

    @classmethod
    @ModelView.button
    @Workflow.transition('done')
    def done(cls, shipments):
        '''
        sale_supply
          - s. .sale.py/SaleLine/get_move (#4292)
          - Moves in sale_supply are strictly only assigned in state staging
          - Since we changed the state of supply moves to draft we have to
            assign the according shipments ourselves.
        '''
        pool = Pool()
        Request = pool.get('purchase.request')
        Sale = pool.get('sale.sale')
        Move = pool.get('stock.move')

        super().done(shipments)
        sales = set()
        purchases = set()
        with Transaction().set_context(_check_access=False):
            move_shipments = ['stock.shipment.in,%s' % s.id for s in shipments]
            moves = Move.search([
                    ('shipment', 'in', move_shipments),
                    ('origin', 'like', 'purchase.line,%'),
                    ])
            purchases.update([m.origin.purchase for m in moves])
            for sub_purchases in grouped_slice(purchases):
                ids = [x.id for x in sub_purchases]
                requests = Request.search([
                        ('purchase_line.purchase.id', 'in', ids),
                        ('origin', 'like', 'sale.sale,%'),
                        ])
                sales.update(r.origin.id for r in requests)
            if sales:
                for sale in sales:
                    sale = Sale(sale)
                    sale.assign_pending_shipments()

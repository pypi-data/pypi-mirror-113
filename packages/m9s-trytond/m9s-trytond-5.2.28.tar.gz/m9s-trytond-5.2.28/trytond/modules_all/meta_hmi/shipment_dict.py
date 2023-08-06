# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from collections import defaultdict

from trytond.pool import PoolMeta, Pool
from trytond.model import ModelView, ModelSQL, fields, DictSchemaMixin


#class OriginInformation(DictSchemaMixin, ModelSQL, ModelView):
class OriginInformation(DictSchemaMixin):
    "Stock Shipment Out Information"
    __name__ = 'stock.shipment.out.information'


class ShipmentOut(metaclass=PoolMeta):
    __name__ = 'stock.shipment.out'

    send_mail_on_shipping = fields.Function(fields.Dict(
            'stock.shipment.out.information',
            'Information'), 'get_send_mail_on_shipping')

    def get_rec_name(self, name):
        field_names = [
            self.number,
            self.customer.rec_name,
            ]
        return ' - '.join(filter(None, field_names))

    @classmethod
    def get_send_mail_on_shipping(cls, shipments, name):
        '''
        E.g. for use in the evaluation of
        - trigger conditions in email templates
          - Check for state 'done'
          - Do not send mail for self pick up
          - Send pick_up mail if no carrier or carrier is our own company
          - Else send delivery mail
        - statements in email templates
          - Provide destination email addresses
          - Provide
        '''
        Sale = Pool().get('sale.sale')

        #res = {s.id: '' for s in shipments}
        #shipments_done = [s for s in shipments if s.state == 'done']
        #for shipment in shipments_done:
        #    res[shipment.id] = 'send'
        #    if shipment.origins:
        #        origin = shipment.origins.split(',')[0]
        #        sales = Sale.search([
        #                ('number', '=', origin),
        #                ])
        #        if sales:
        #            sale = sales[0]
        #            if sale.self_pick_up:
        #                res[shipment.id] = 'self_pick_up'
        #            elif (sale.carrier and
        #                    sale.carrier.party.id == shipment.company.party.id):
        #                res[shipment.id] = 'pick_up'

        res = {s.id: defaultdict('') for s in shipments}
        shipments_done = [s for s in shipments if s.state == 'done']
        for shipment in shipments_done:
            res[shipment.id]['action'] = 'send'
            if shipment.origins:
                origin = shipment.origins.split(',')[0]
                sales = Sale.search([
                        ('number', '=', origin),
                        ])
                if sales:
                    sale = sales[0]
                    if sale.self_pick_up:
                        res[shipment.id]['action'] = 'self_pick_up'
                    elif (sale.carrier
                            and sale.carrier.party.id == shipment.company.party.id):
                        res[shipment.id]['action'] = 'pick_up'
        print(res)
        return res
        # Equal(Get(Eval('self', {}), 'send_mail_on_shipping', ''), 'send')
        # Equal(Get(Eval('self', {}), Get(Eval('send_mail_on_shipping', {}), 'action', ''), ''), 'send')



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

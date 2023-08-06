# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from decimal import Decimal
from datetime import datetime, timedelta

from trytond.config import config
from trytond.model import fields, Workflow, ModelView
from trytond.pyson import Eval, In

from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond import backend
from nereid.contrib.locale import make_lazy_gettext
from nereid.ctx import has_request_context
from nereid import current_website

_ = make_lazy_gettext('meta_hmi')

shop_delivery_time_shift = config.get('nereid_webshop',
    'shop_delivery_time_shift')

BW_holidays = {}
try:
    import holidays
    for date, name in sorted(holidays.DE(
                state='BW', years=datetime.now().year).items()):
        BW_holidays[date] = name
except ImportError:
    pass


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    cash_on_pickup = fields.Boolean('Cash on Pickup/Bank Transfer/Credit Card')
    comment_hint = fields.Function(fields.Char('Comment hint',
            states={
                'invisible': ~Eval('comment', True),
                }, readonly=True,
            depends=['comment']), 'get_comment_hint')
    # confirmation_url is filled at a time we are still under application
    # context (to be used later in the confirmation email sent by workers
    # without app context)
    confirmation_url = fields.Char('Confirmation URL',
        depends=['guest_access_code'])
    party_comment = fields.Function(fields.Text("Party Comment"),
        'get_party_comment', setter='set_party_comment')
    webshop_mail_state = fields.Function(fields.Char('Webshop Mail State',
            depends=['state']),
            'get_webshop_mail_state')

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        cls.channel.states['readonly'] = Eval('state') != 'draft'
        cls.cash_on_pickup.states = cls.self_pick_up.states
        cls._transitions |= set((
            ('confirmed', 'quotation'),
            ('draft', 'processing'),
            ('quotation', 'processing'),
            # needed to be able to handle stuck worker processes,
            # e.g. failed web payments, queue processing
            ('processing', 'quotation'),
            ))
        cls._buttons.update({
                'to_quote': {
                     'invisible': (
                        ~(Eval('state').in_(['confirmed', 'processing'])) |
                        (Eval('state').in_(['confirmed', 'processing'])) &
                        (Eval('invoice_state') != 'none') &
                        (Eval('shipping_state') != 'none')
                        ),
                     },
                'express_process': {
                    'invisible': In(Eval('state'), ['cancel', 'done'],)
                    },
                'express_process_print': {
                    'invisible': In(Eval('state'), ['cancel', 'done'],)
                    },
                'add_payment': {
                    'invisible': (
                        (In(Eval('state'), ['cancel', 'done'])) |
                        (Eval('invoice_state') == 'paid')
                        ),
                    },
                 })
        # Set the necessary values for the computation of the
        # customer price to the context of field 'lines'
        cls.lines.context['currency'] = Eval('currency')
        cls.lines.context['customer'] = Eval('party')
        cls.lines.context['sale_date'] = Eval('sale_date')
        cls.lines.context['price_list'] = Eval('price_list')

        cls.comment_allowed_states += ['quotation']

    def get_rec_name(self, name=None):
        '''
        '''
        res = self.party.full_name
        if self.number:
            res += ' - %s' % (self.number,)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        '''
        sale
          - extend to search always also for party (#2888)
        '''
        domain = super(Sale, cls).search_rec_name(name, clause)
        _, operator, value = clause
        domain.append(('party', operator, value))
        return domain

    @classmethod
    def get_webshop_mail_state(cls, sales, name):
        '''
        For use in the evaluation of trigger conditions in email templates.

        Return the current state if
        - channel is webshop
        - all lines have a positive amount
        '''
        send_states = {}
        for sale in sales:
            if (sale.channel_type == 'webshop'
                    and not any([l for l in sale.lines
                        if l.amount < Decimal('0.0')])):
                    send_states[sale.id] = sale.state
            else:
                send_states[sale.id] = ''
        return send_states

    def get_comment_hint(self, name):
        if self.comment:
            return self.comment[:120].replace('\n', ' ').replace('\r', ' ')

    def get_party_comment(self, name=None):
        if self.party:
            return self.party.description
        return None

    @classmethod
    def set_party_comment(cls, sales, name, value):
        pool = Pool()
        Party = pool.get('party.party')
        if not value:
            return
        for sale in sales:
            Party.write([sale.party], {
                    'description': value,
                    })

    @classmethod
    @ModelView.button
    @Workflow.transition('quotation')
    def to_quote(cls, sales):
        pass

    @classmethod
    @ModelView.button
    @Workflow.transition('quotation')
    def quote(cls, sales):
        if shop_delivery_time_shift:
            for sale in [s for s in sales if s.channel.source == 'webshop']:
                sale.set_shop_delivery_date()
        super(Sale, cls).quote(sales)

    def set_shop_delivery_date(self):
        '''
        HMI:
        Set the requested_delivery_date to the next day (instead of today),
        if the order comes from the webshop and is confirmed past the defined
        time. (#3025)
        '''
        pool = Pool()
        Date = pool.get('ir.date')

        today = Date.today()
        next_delivery_day = today + timedelta(days=1)
        # weekends and holidays
        weekend = False
        while ((next_delivery_day in list(BW_holidays.keys())) or
                (next_delivery_day.weekday() >= 5)):
                    weekend = True
                    next_delivery_day += timedelta(days=1)

        now = datetime.utcnow()
        datetime_limit = datetime.combine(now.date(),
            datetime.strptime(shop_delivery_time_shift,'%H%M').time())

        for line in self.lines:
            if (line.shipping_date and
                    line.shipping_date <= today):
                # Set next_delivery_day when date_time_limit has passed
                # and on weekends
                if (now > datetime_limit or weekend):
                    line.requested_delivery_date = next_delivery_day
                    line.save()

    def print_sale_invoice(self):
        pool = Pool()
        InvoiceReport = pool.get('account.invoice', type='report')
        User = pool.get('res.user')
        invoice_ids = [invoice.id for invoice in self.invoices if
                invoice.state != 'cancel']
        if invoice_ids:
            transaction = Transaction()
            context = transaction.context
            user = User(transaction.user)
            print_context = context.copy()
            print_context['auto_print'] = True
            for invoice_id in invoice_ids:
                print_context['active_ids'] = [invoice_id]
                print_context['active_id'] = invoice_id
                with transaction.set_context(print_context):
                    InvoiceReport.execute([invoice_id], {})

    @classmethod
    def _get_queue_context(cls):
        return {
            'skip_credit_check': True,
            'skip_volume_weight_check': True,
            'skip_stock_pickup_check': True,
            'queue_name': 'sale_express_process',
            }

    @classmethod
    def _express_process(cls, sales):
        cls.prevalidate_sales(sales)
        # We *must* quote before entering the queue, because we can not reset
        # to draft inside the queue with module product_kit.
        cls.quote([s for s in sales if s.state == 'draft'])
        # We write the workflow state for convenience in tht UI display.
        cls.write(sales, {'state': 'processing'})

    @classmethod
    @ModelView.button
    @Workflow.transition('processing')
    def express_process(cls, sales):
        cls._express_process(sales)
        context = cls._get_queue_context()
        with Transaction().set_context(**context):
            cls.__queue__.queue_express_process(sales)

    @classmethod
    @ModelView.button
    @Workflow.transition('processing')
    def express_process_print(cls, sales):
        cls._express_process(sales)
        context = cls._get_queue_context()
        with Transaction().set_context(**context):
            cls.__queue__.queue_express_process(sales,
                print_invoice=True)

    @classmethod
    def queue_express_process(cls, sales, print_invoice=False):
        # The sale is immediately set to state processing by workflow
        # transition, so we reset the start state which in our case must be
        # quotation.
        # We must start from quotation, because module product_kit
        # strictly depends on correct states.
        # (Resetting to quotation by workflow triggers errors
        # with quote in module product_kit (#4300, #4302))
        cls.write(sales, {'state': 'quotation'})
        cls.preprocess_sales(sales)
        cls.finalize_workflow(sales)
        cls.postprocess_sales(sales, print_invoice=print_invoice)

    @classmethod
    def prevalidate_sales(cls, sales):
        '''
        Run all procedures needed before entering the queue
        - checks that will workers let fail due to user warnings
        - set the sale date, that must be set before leaving the
          workflow transition (the transition delegates after
          prevalidate to the queue, so it doesn't help if it
          is set inside the queue)
        '''
        pool = Pool()
        Warning = pool.get('res.user.warning')

        for sale in [s for s in sales if s.state in ['draft', 'quotation']]:
            sale.party.check_credit_limit(sale.untaxed_amount,
                origin=str(sale))

            # We have to take care ourselves for UserWarning inside the
            # transaction. If there exist warnings, i.e. checks were already
            # skipped, we do not check again and clean up
            warning_name = 'missing_weight_volume_sale_%s' % sale.id
            if Warning.check(warning_name):
                sale.check_volume_weight()

            cls.check_stock([sale])
            cls.set_sale_date([sale])

    @classmethod
    def finalize_workflow(cls, sales):
        to_quote = []
        to_confirm = []
        to_process = []
        for sale in sales:
            if sale.state == 'draft':
                to_quote.append(sale)
            elif sale.state == 'quotation':
                to_confirm.append(sale)
            elif sale.state == 'confirmed':
                to_process.append(sale)
        to_confirm += to_quote
        to_process += to_confirm
        if to_quote:
            cls.quote(to_quote)
        if to_confirm:
            cls.confirm(to_confirm)
        # we must run process directly here to get it done before calling
        # the printout
        if to_process:
            cls.process(to_process)

    @classmethod
    def preprocess_sales(cls, sales):
        cls.set_number(sales)
        # Authorize and capture pending payments
        for sale in sales:
            # Capture authorized web sales
            if sale.is_cart and sale.payment_authorized:
                sale.payment_processing_state = 'waiting_for_capture'
                sale.process_pending_payments()
                continue
            # Authorize and capture all payments waiting for authorization
            capture = None
            if sale.payment_processing_state == 'waiting_for_auth':
                capture = True
            if sale.payment_processing_state is not None:
                sale.process_pending_payments()
                # If we authorized in the first step, we capture now
                if capture:
                    sale.payment_processing_state = 'waiting_for_capture'
                    sale.process_pending_payments()

    @classmethod
    def postprocess_sales(cls, sales, print_invoice=False):
        for sale in sales:
            sale.settle_manual_payments()
            sale.post_pending_invoices()
            sale.assign_pending_shipments()
            sale.process_pending_transactions()

            sale.reprocess_paid_invoices()
            if print_invoice:
                sale.print_sale_invoice()
            # No need to (re-)process payments, all should be done
            if sale.is_done() and sale.payment_processing_state:
                sale.payment_processing_state = None

    @fields.depends(methods=['on_change_lines'])
    def on_change_self_pick_up(self):
        '''
        sale_pos_channel
          - unset the carrier for self pickup
        '''
        super(Sale, self).on_change_self_pick_up()
        if self.self_pick_up:
            self.carrier = None

    def get_weight_uom(self, name):
        '''
        shipping/sale.py

        - Use a European default
        '''
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_gram')

    def create_shipment(self, shipment_type):
        '''
        get_sale_price is called from here, we need to set the context
        '''
        context = Transaction().context.copy()
        context['sale'] = self
        with Transaction().set_context(context):
            super(Sale, self).create_shipment(shipment_type)

    def set_shipment_cost(self):
        '''
        sale
        - monkey patch for the only purpose, that we also want to get
          shipping lines with amount 0.
        - updated for https://tryton-rietveld.appspot.com/26151002
          (s.a. issue6273_sale_shipment_cost_delete_old_cost_lines.patch)
        - 20200214: Use get_shipping_rates in precedence of
                    cost calculation by carrier to get the same prices as on
                    the web. If there is no rate available (i.e. the carrier
                    was selected manually on a sale) fall back to the ususal
                    carrier calculation. #3767
        - 20200220: Print the service type on the cost line description
        '''
        pool = Pool()
        Date = pool.get('ir.date')
        Currency = pool.get('currency.currency')

        cost, currency_id = 0, None
        ### 20200214 ->
        shipping_rates = self.get_shipping_rates()
        if self.carrier:
            for rate in shipping_rates:
                if rate['carrier'] == self.carrier:
                    cost = rate['cost']
                    currency_id = rate['cost_currency'].id
                    break
            if currency_id is None:
        ### 20200214 <-
                with Transaction().set_context(self._get_carrier_context()):
                    cost, currency_id = self.carrier.get_sale_price()

        cost_line = None
        products = [line.product for line in self.lines or []
                if getattr(line, 'product', None)]
        stockable = any(product.type in ('goods', 'assets', 'kit')
            for product in products)
        ###### ->
        if currency_id and stockable:
        ###### <-
            today = Date.today()
            date = self.sale_date or today
            with Transaction().set_context(date=date):
                cost = Currency.compute(Currency(currency_id), cost,
                    self.currency)
            cost_line = self.get_shipment_cost_line(cost)
            ###### 20200220 ->
            if self.carrier.service_type:
                cost_line.description = ' - '.join(
                    [cost_line.description, self.carrier.service_type])
            ###### 20200220 <-

        removed = []
        lines = list(self.lines or [])
        for line in self.lines:
            if line.type == 'line' and line.shipment_cost is not None:
                # Diverging from upstream we keep already created cost
                # lines and thus the possibility to have custom amounts
                # for shipment costs
                # lines.remove(line)
                # removed.append(line)
                if cost_line:
                    line.sequence = cost_line.sequence
                    cost_line = None
        if cost_line:
            lines.append(cost_line)
        self.lines = lines
        return removed

    def get_shipping_rates(self, carriers=None, silent=False):
        '''
        shipping

        Starting from the use of
        issue2612_carrier__sale_shipment_cost_carrier_selection.patch
        we override completely to make use of sale.available_carriers
        (country specific list of carriers)

         - Add meta informations to the rates: Default carrier
         - Only use the product name for the displayed value
         - Sort the displayed list on costs
        '''
        pool = Pool()
        ModelData = pool.get('ir.model.data')
        UOM = pool.get('product.uom')

        # Get shipping rates and default carrier (it is the first one returned
        # according to sequence on carrier.selection)
        rates = []
        default_carrier = None
        for number, carrier in enumerate(self.available_carriers):
            rates.extend(self.get_shipping_rate(carrier, silent=silent))
            if number == 0:
                default_carrier = carrier
        # Now sort the rates after the price for a convenient display
        sorted_rates = sorted(rates, key=lambda k: k['cost'])  # , reverse=True)

        # Follows a complete overide of carrier price calculation
        # This is subject to a new future implementation of shipping
        # costs based on length, additional costs, etc. #3783
        additional_insurance = None
        if self.total_amount > Decimal('750'):
            additional_insurance = True
        #if any([l.amount > Decimal('250') for l in self.lines]):
        #    print('amount>250')

        # GLS laengste + kuerzeste Seite
        # XS 35cm
        # S  50cm
        # M  70cm
        # L  90cm
        # XL 300cm²
        over_length = {}
        product_lengths = [
            (l.product.length, l.product.length_uom) for l in self.lines
            if l.product
            and l.product.type == 'goods'
            and l.product.length]

        # Convert UOM to cm and find max_length
        max_length = 0
        uom_cm = UOM(ModelData.get_id('product', 'uom_centimeter'))
        for length, uom in product_lengths:
            length_cm = UOM.compute_qty(uom, length, uom_cm)
            max_length = max(length_cm, max_length)

        # Select over_length service for max_length
        if max_length > 75:  # XL
            over_length['size'] = 'XL'
            over_length['price'] = Decimal('18.90')
        elif max_length > 55:  # L
            over_length['size'] = 'L'
            over_length['price'] = Decimal('9.90')
        elif max_length > 35:  # M
            over_length['size'] = 'M'
            over_length['price'] = Decimal('6.30')
        # Add ususal packaging cost
        if over_length:
            over_length['price'] += Decimal('3.00')

        free_shipping = self.get_free_shipping()
        final_rates = []
        for rate in sorted_rates:
            # Always offer pickup
            if 'Abholung' in rate['display_name']:
                final_rates.append(rate)
                continue
            carrier = rate['carrier']
            if carrier == default_carrier:
                rate['default_carrier'] = True
            carrier_name = carrier.carrier_product.rec_name
            if carrier.service_type:
                carrier_name = ' - '.join(
                    [carrier.carrier_product.rec_name, carrier.service_type])
            rate['display_name'] = carrier_name

            # Additinal insurance: get a quote
            if additional_insurance:
                if rate['carrier'] == default_carrier:
                    rate['cost'] = Decimal('0.0')
                    rate['display_name'] = u'Diese Sendung muss höher versichert werden. Bitte wählen Sie im nächsten Schritt Überweisung, wir senden Ihnen ein individuelles Angebot zu.'
                    final_rates.append(rate)
                    continue
                else:
                    continue

            # Over length only as insured package or pickup
            if over_length:
                if 'Abholung' in rate['display_name']:
                    final_rates.append(rate)
                    continue
                elif rate['carrier'] == default_carrier:
                    rate['cost'] = over_length['price']
                    rate['display_name'] += ' ' + over_length['size']
                    final_rates.append(rate)
                    continue
                else:
                    continue

            if free_shipping and 'Fahrrad' not in carrier_name:
                rate['cost'] = Decimal('0.0')
            final_rates.append(rate)
        return final_rates

    def get_free_shipping(self):
        if (self.channel.free_shipping_limit
                and self.shipment_address.country.code == 'DE'):
            net_amount = sum([line.amount for line in self.lines
                    if line.type == 'line'
                    and not line.shipment_cost])
            if net_amount >= self.channel.free_shipping_limit:
                return True
        return False

    def _add_sale_payment(self, credit_card_form=None, payment_profile=None,
            alternate_payment_method=None):
        '''
        nereid_checkout
          - Document the used gateway in the sale description
          - Do not create any payments for gateways marked 'defer_payment'
            (Cash on Pickup)
            Note:
                20190614: #3492
                Stripe gateways have to be set to defer, because payments and
                transactions are already created and otherwise duplicated!!
        '''
        def add_description(text):
            if self.description:
                self.description += ', ' + text
            else:
                self.description = text

        if alternate_payment_method:
            add_description(alternate_payment_method.gateway.rec_name)
            if alternate_payment_method.gateway.defer_payment:
                # For now we can not use self_pickup, because it moves the
                # products directly to Done (#2607)
                self.cash_on_pickup = True
                # Two possibilities to be able to assign the ordered items:
                # - Change the shipment creation to on order (risks to deliver
                #   unpaid orders by accident, but assigns automatically after
                #   processing the sale)
                # - Pay manually and preliminarily via a manual gateway not
                #   marked defer_payment (takes several manual steps)
                self.shipment_method = 'order'
        elif credit_card_form:
            add_description(current_website.credit_card_gateway.rec_name)
            self.cash_on_pickup = True
        self.save()

        return super(Sale, self)._add_sale_payment(
            credit_card_form=credit_card_form,
            payment_profile=payment_profile,
            alternate_payment_method=alternate_payment_method)

    def handle_payment_on_confirm(self):
        '''
        sale_payment_gateway
          - Skip payment processing for Cash on Pickup
        '''
        if self.cash_on_pickup:
            return
        super(Sale, self).handle_payment_on_confirm()

    def handle_payment_on_process(self):
        '''
        sale_payment_gateway
          - Skip payment processing for Cash on Pickup
        '''
        if self.cash_on_pickup:
            return
        super(Sale, self).handle_payment_on_process()

    def settle_manual_payments(self):
        '''
        Complete override
        sale_payment_gateway, gift_card
          - Skip transaction creation for gateways with defer_payment
          - Also cleanup empty transactions
        '''
        pool = Pool()
        SalePayment = pool.get('sale.payment')

        for payment in self.payments:
            if (payment.amount_available
                    and payment.method in ['manual', 'gift_card']
                    and not payment.payment_transactions
                    and not payment.gateway.defer_payment):
                payment_transaction = payment._create_payment_transaction(
                    payment.amount_available,
                    str(_('Post manual payments on Processing Order')),
                )
                payment_transaction.save()
                payment.capture()
                self.payment_processing_state = None
        # Cleanup empty payments (i.e. without transactions) on paid sales,
        # that may exist after adding payments with the payment wizard.
        # For now we only check for payments from gateways marked
        # defer_payment. #3007
        if self.payment_collected >= self.total_amount:
            payments_to_delete = []
            for payment in [p for p in self.payments if
                    p.gateway.defer_payment]:
                if not payment.payment_transactions:
                    payments_to_delete.append(payment)
            if payments_to_delete:
                SalePayment.delete(payments_to_delete)

    @classmethod
    def process_all_pending_payments(cls):
        '''
        sale_payment_gateway
        - Settle manual gateway payments for already processed sales.
        - Post invoices for processed sales.
        - Process pending payment transactions.

        - Reprocess Paypal payments (#2839)

        - For convenience also run assign_all_pending_shipments here instead of
          creating a separate cron job.
        '''
        OperationalError = backend.get('DatabaseOperationalError')

        super(Sale, cls).process_all_pending_payments()
        sales = cls.search([
            ('payment_capture_on', '=', 'manual'),
            ('invoice_state', '!=', 'paid'),
            ('state', 'in', ['confirmed', 'processing']),
        ])
        for sale in sales:
            sale.settle_manual_payments()
            sale.post_pending_invoices()
            sale.process_pending_transactions()
        # Reprocess sales with paid Paypal payments
        sales = cls.search([
            ('channel', '=', 'webshop'),
            ('state', '=', 'processing'),
        ])
        for sale in sales:
            sale.reprocess_paid_invoices()
        # Instead of creating a separate cron job we run for convenience here
        # Wrap into try...except to handle exceptions on locks on the
        # stock_move table
        try:
            cls.assign_all_pending_shipments()
        except OperationalError as e:
            print(('assign_all_shipments: %s' % (e.message,)))
            pass

    def post_pending_invoices(self):
        '''
        Post all draft invoices.
        '''
        Invoice = Pool().get('account.invoice')

        invoices_to_post = [invoice for invoice in self.invoices
            if invoice.state == 'draft']
        if invoices_to_post:
            Invoice.post(invoices_to_post)

    def reprocess_paid_invoices(self):
        '''
        Reprocess all paid invoices.
         - Needed to set the correct sale state after an invoice is reconciled
           by a payment transaction (#2839, #3041).
        '''
        Invoice = Pool().get('account.invoice')

        if self.state == 'processing':
            # XXX Still needed? #3041
            #if self.payment_collected >= self.total_amount:
            #    # Ugly hack to bypass this blocking state caused by some
            #    # step earlier
            #    self.payment_processing_state = None
            #    self.save()
            invoices_to_process = [invoice for invoice in self.invoices
                if invoice.state == 'paid']
            if invoices_to_process:
                Invoice.process(invoices_to_process)

    @classmethod
    def assign_all_pending_shipments(cls):
        '''
        Assign all shipments of sales in state processing.
        '''
        sales = cls.search([
            ('state', '=', 'processing'),
        ])
        for sale in sales:
            sale.assign_pending_shipments()

    def assign_pending_shipments(self):
        '''
        Assign the shipments of a sale.
        '''
        ShipmentOut = Pool().get('stock.shipment.out')
        shipments_to_assign = [shipment for shipment in self.shipments
            if shipment.state in ['draft', 'waiting']]
        ShipmentOut.assign_try(shipments_to_assign)

    def process_pending_transactions(self):
        '''
        Reconcile all pending gateway payments (Cash gateway).
        Uses invoice_payment_gateway/pay_using_transaction:
            - write payment lines
            - reconcile if possible
            - do not try to pay already paid invoices
        '''
        transactions = [txn for txn in self.gateway_transactions if txn.move]
        for transaction in transactions:
            invoices = [inv for inv in self.invoices if inv.state != 'paid']
            for invoice in invoices:
                invoice.pay_using_transaction(transaction)

    def process_manual_payment(self, amount):
        # create payment and transaction
        self.authorize_payments(amount,
            description=str(_('Manual payment from sale')))
        # capture the payment directly
        self.payment_processing_state = "waiting_for_capture"
        self.process_pending_payments()
        # reconcile related invoices if existent
        if self.state == 'processing':
            self.process_pending_transactions()

    @classmethod
    def delete_old_carts(cls):
        '''
        Delete carts older than a year.
        '''
        Date = Pool().get('ir.date')

        today = Date.today()
        to_date = datetime.combine(today - timedelta(days=365),
            datetime.min.time())
        to_delete = cls.search([
            ('state', '=', 'draft'),
            ('is_cart', '=', True),
            ('create_date', '<', to_date),
        ])
        if to_delete:
            # - Remove any carriers that could cause domain
            # validation errors
            # - Cancel all sales, before trying to delete them and do not fail
            # on those with related records (#3888)
            with Transaction().set_context(skip_check_user_channel=True):
                cls.write(to_delete, {
                        'carrier': None,
                        'state': 'cancel',
                        })
                for sale in to_delete:
                    try:
                        cls.delete([sale])
                    except:
                        pass


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()
        # Set a value in the context to be recognized for get_rec_name
        # of products on sale views
        cls.product.context['with_quantity'] = True

    @staticmethod
    def default_quantity():
        return 1

    @fields.depends('product')
    def on_change_product(self):
        # Set line description before super, because product_kit needs it
        if self.product:
            self.description = self.product.name
        super(SaleLine, self).on_change_product()

    @property
    def supply_on_sale(self):
        '''
        sale_supply/sale.py
          - Run sale_supply only
            - when there is no stock for the product
              TODO:
              - in case there is stock, but not enough to satisfy the ordered
                quantity, the purchase will have to go through force_assign of
                the customer shipment for missing stock: perhaps to be catched
                later, should be rarely the case
            - when the product is of type goods (no shipping services)
            - when the stock of the product is not
              managed by an order point
        '''
        OrderPoint = Pool().get('stock.order_point')

        supply_on_sale = super(SaleLine, self).supply_on_sale
        if supply_on_sale:
            if (self.available_stock_qty > 0 or self.product.type != 'goods'):
                supply_on_sale = False
            if supply_on_sale:
                order_point = OrderPoint.search([
                        ('product', '=', self.product.id),
                        ])
                if order_point:
                    supply_on_sale = False
        return supply_on_sale

    def get_move(self, shipment_type):
        '''
        sale_supply
          - Moves in state staging can not be assigned later by then available
            stock.
          - Purchase requests for moves in state staging are forcefully
            regenerated when deleted and must be processed to get them out of
            the system
        Therefore we put state 'draft' on those moves (#4292).
        S. a. .shipment/ShipmentIn assignation on done.
        '''
        move = super().get_move(shipment_type)
        if move and move.state == 'staging':
            move.state = 'draft'
        return move


class AddSalePayment(metaclass=PoolMeta):
    __name__ = 'sale.payment.add'

    def create_sale_payment(self, profile=None):
        '''
        sale_payment_gateway
          - we must reset authorization and capture settings of the channel to
            some automated setting in case we use a card (if those settings are
            set to 'manual' payments by card will not be processed) #2719
          - we have to set this early to prevent the wizard from failing with
            KeyError: None when extending transition_add #2739
        '''
        pool = Pool()
        Sale = pool.get('sale.sale')
        SaleConfiguration = pool.get('sale.configuration')
        sale = Sale(Transaction().context.get('active_id'))

        if self.payment_info.method == 'credit_card':
            if sale.payment_authorize_on == 'manual':
                authorize_on = SaleConfiguration(1).payment_authorize_on
                if authorize_on == 'manual':
                    authorize_on = 'sale_confirm'
                sale.payment_authorize_on = authorize_on
            if sale.payment_capture_on == 'manual':
                capture_on = SaleConfiguration(1).payment_capture_on
                if capture_on == 'manual':
                    capture_on = 'sale_process'
                sale.payment_capture_on = capture_on
            sale.save()
        return super(AddSalePayment, self).create_sale_payment(profile=profile)

    def transition_add(self):
        '''
        sale_payment_gateway
          - Add a transaction to the payment (super only creates the payment)
          - Process the whole transaction immediately so we don't have to wait
            for the cron job.
          - BEWARE: Don't do this for payments from the web (like PayPal or
            Stripe), otherwise we end with multiple transactions #2889
            or break the authorization workflow.
        '''
        Sale = Pool().get('sale.sale')

        res = super(AddSalePayment, self).transition_add()
        # Process payments at once when performed manually from the client
        if not has_request_context():
            sale = Sale(Transaction().context.get('active_id'))
            Sale.__queue__.process_manual_payment(sale,
                self.payment_info.amount)
        return res

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import json
import http.client
import logging
import stripe

from flask_wtf import FlaskForm as Form

from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.modules.nereid_checkout.checkout import not_empty_cart, \
    sale_has_non_guest_party, with_company_context

from nereid import Response
from nereid import render_template, request, url_for, flash, redirect, \
    current_user, current_locale, route, abort
from nereid.contrib.locale import make_lazy_gettext


_ = make_lazy_gettext('meta_hmi')

logger = logging.getLogger(__name__)


class Cart(metaclass=PoolMeta):
    __name__ = 'nereid.cart'

    def get_alternate_payment_methods(self):
        '''
        nereid_checkout
          - Define custom filters
            e.g. cash payment only when self pickup
        CAVEAT: Depends on the exact defined items
        '''
        payment_methods = self.website.alternate_payment_methods
        pickup_product_name = 'Abholung / Gutschein per E-Mail'
        payment_name = 'Barzahlung'
        if self.sale.carrier.carrier_product.name != pickup_product_name:
            filtered_methods = []
            for method in payment_methods:
                if method.name == payment_name:
                    continue
                filtered_methods.append(method)
            payment_methods = filtered_methods
        return payment_methods


class FakeCreditCardForm(Form):
    '''
    nereid_checkout
    Just supply an empty form for template logic.
    '''


class Checkout(metaclass=PoolMeta):
    __name__ = 'nereid.checkout'

    @classmethod
    def get_credit_card_form(cls):
        '''
        nereid_checkout
          - Use our custom form
        '''
        return FakeCreditCardForm()

    @classmethod
    @route('/checkout/shipping-address', methods=['GET', 'POST'])
    @not_empty_cart
    @sale_has_non_guest_party
    def shipping_address(cls):
        '''
        nereid_checkout
        - Adds handling for use_shipment_address
        - Cleanup of carriers evtl. not matching a different address domain
        Q&D:
        - Use the name provided on shipping address to update the party
        - Set the default language of the party
          (should be on sign-in, done for simplicity here))
        '''
        pool = Pool()
        NereidCart = pool.get('nereid.cart')
        Address = pool.get('party.address')
        Date = pool.get('ir.date')

        cart = NereidCart.open_cart()

        address = None
        if current_user.is_anonymous and cart.sale.shipment_address:
            address = cart.sale.shipment_address

        address_form = cls.get_new_address_form(address)

        if request.method == 'POST':

            use_shipment_address = False

            if not current_user.is_anonymous and request.form.get('address'):
                # Registered user has chosen an existing address
                address = Address(request.form.get('address', type=int))
                use_shipment_address = request.form.get('use_shipment_address')

                if address.party != cart.sale.party:
                    flash(_('The address chosen is not valid'))
                    return redirect(
                        url_for('nereid.checkout.shipping_address')
                    )

            else:
                # Guest user or registered user creating an address. Only
                # difference is that the party of address depends on guest or
                # not
                if not address_form.validate():
                    address = None
                else:
                    if current_user.is_anonymous and \
                            cart.sale.shipment_address:
                        # Save to the same address if the guest user
                        # is just trying to update the address
                        address = cart.sale.shipment_address
                    else:
                        address = Address()

                    party = cart.sale.party
                    address.party = party
                    # Try to parse the address name into name and first_name
                    # and use it on party
                    names = address_form.name.data.split(' ')
                    if names:
                        if party.name:
                            desc = party.description or ''
                            if desc:
                                desc += '\n'
                            desc += str(Date.today()) + ': ' + party.name
                            party.description = desc
                        party.name = names[-1]
                        if len(names) > 1:
                            party.first_name = names[-2]
                        else:
                            party.first_name = None
                        party.lang = current_locale.language
                    address.party_name = address_form.name.data
                    address.street = address_form.street.data
                    address.zip = address_form.zip.data
                    address.city = address_form.city.data
                    address.country = address_form.country.data
                    address.subdivision = address_form.subdivision.data

                    if address_form.phone.data:
                        phone = \
                            cart.sale.party.add_contact_mechanism_if_not_exists(
                                'phone', address_form.phone.data
                            )
                        address.phone = address_form.phone.data
                    address.save()
                    # Set the vat_code according to the selected legal form
                    if address_form.company.data:
                        party.party_type = 'organization'
                        if address_form.vat_id.data:
                            vat_code = party.manage_vat_code(
                                address_form.vat_id.data)
                    else:
                        party.party_type = 'person'
                        vat_code = party.manage_vat_code(None)
                    party.save()
                    use_shipment_address = request.form.get(
                        'use_shipment_address')

            if address is not None:
                cart.sale.shipment_address = address
                if use_shipment_address:
                    cart.sale.invoice_address = cart.sale.shipment_address
                # Cleanup any carriers, that could conflict with the domain
                # of a possibly different address country introduced by
                # issue2612_carrier__sale_shipment_cost_carrier_selection.patch
                # (#2923)
                cart.sale.carrier = None
                cart.sale.save()
                # Reprocess sale lines to get correct taxes according to
                # destination country
                cart.sale.reprocess_sale_lines()

                if use_shipment_address:
                    return redirect(url_for('nereid.checkout.validate_address'))
                else:
                    return redirect(url_for('nereid.checkout.billing_address'))

        addresses = []
        if not current_user.is_anonymous:
            addresses.extend(current_user.party.addresses)

        return render_template(
            'checkout/shipping_address.jinja',
            addresses=addresses,
            address_form=address_form,
            )

    @classmethod
    @route('/checkout/validate-address', methods=['GET', 'POST'])
    @not_empty_cart
    @sale_has_non_guest_party
    def validate_address(cls):
        '''
        nereid_checkout

        Implements for our custom workflow:
            - first get addresses
            - delivery options
            - payment options

        Not yet implemented: template and POST for more validation, address
        suggestions etc.
        '''
        NereidCart = Pool().get('nereid.cart')

        cart = NereidCart.open_cart()

        if not cart.sale.shipment_address:
            return redirect(url_for('nereid.checkout.shipping_address'))

        if not cart.sale.invoice_address:
            return redirect(url_for('nereid.checkout.billing_address'))

        return redirect(url_for('nereid.checkout.delivery_method'))

    @classmethod
    def preprocess_confirm_cart(cls, cart):
        '''
        Run here any procedures needed before entering the queue (e.g. that
        need the request context)
        '''
        super(Checkout, cls).preprocess_confirm_cart(cart)
        sale = cart.sale
        if sale:
            sale.confirmation_url = url_for('sale.sale.render',
                active_id=sale.id, access_code=sale.guest_access_code,
                _external=True)
            sale.save()
            cart.save()

    @classmethod
    @route('/checkout/webhook/stripe/<identifier>', methods=['POST'],
        exempt_csrf=True)
    @with_company_context
    def webhook_endpoint(cls, identifier):
        pool = Pool()
        PaymentGateway = pool.get('payment_gateway.gateway')

        gateway, = PaymentGateway.search([
                ('stripe_webhook_identifier', '=', identifier),
                ], limit=1)
        secret = gateway.stripe_webhook_signature_secret_key
        if secret:
            sig_header = request.headers['STRIPE_SIGNATURE']
            request_body = request.get_data(as_text=True)
            try:
                stripe.Webhook.construct_event(
                    request_body, sig_header, secret)
            except ValueError:  # Invalid payload
                abort(http.client.BAD_REQUEST)
            except stripe.error.SignatureVerificationError:
                abort(http.client.BAD_REQUEST)
        else:
            logger.warn("Stripe signature ignored")

        payload = json.loads(request_body)
        result = cls.webhook(payload)
        if result is None:
            logger.info("No callback for payload type '%s'", payload['type'])
        elif not result:
            return Response(status=http.client.NOT_FOUND)
        return Response(status=http.client.NO_CONTENT)

    @classmethod
    def webhook(cls, payload):
        '''
        This method dispatches stripe webhook callbacks

        The return values are:
            - None if there is method defined to handle the payload type
            - True if the payload has been handled
            - False if the payload could not be handled
        '''
        data = payload['data']
        type_ = payload['type']
        if type_ == 'charge.succeeded':
            return cls.webhook_charge_succeeded(data)
        if type_ == 'charge.captured':
            return cls.webhook_charge_captured(data)
        elif type_ == 'charge.failed':
            return cls.webhook_charge_failed(data)
        elif type_ == 'charge.pending':
            return cls.webhook_charge_pending(data)
        elif type_ == 'charge.refunded':
            return cls.webhook_charge_refunded(data)
        elif type_ == 'charge.dispute.created':
            return cls.webhook_charge_dispute_created(data)
        elif type_ == 'charge.dispute.closed':
            return cls.webhook_charge_dispute_closed(data)
        #elif type_ == 'source.chargeable':
        #    return cls.webhook_source_chargeable(data)
        #elif type_ == 'source.failed':
        #    return cls.webhook_source_failed(data)
        #elif type_ == 'source.canceled':
        #    return cls.webhook_source_canceled(data)
        return None

    @classmethod
    def webhook_charge_succeeded(cls, payload, _event='charge.succeeded'):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')

        charge = payload['object']
        transactions = PaymentTransaction.search([
                ('provider_reference', '=', charge['payment_intent']),
                ('state', '!=', 'posted'),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error("%s: No Transactions for Payment Intent '%s'", _event,
                charge['payment_intent'])
        # When multiple transactions were found we take the last one.
        elif len(transactions) > 1:
            logger.error("%s: Multiple Transactions for Payment Intent '%s'",
                _event, charge['payment_intent'])
        if transactions:
            transaction = transactions[0]
            with Transaction().set_context(company=transaction.company.id):
                # The webhook can be sent for a former unsuccessful
                # charge (e.g. error in 3D autorisation) which means there can
                # exist failed transcations for the same intent.
                # If we don't find another posted transaction we create a new
                # one that will succeed.
                if transaction.state == 'failed':
                    posted_transactions = PaymentTransaction.search([
                            ('provider_reference', '=',
                                charge['payment_intent']),
                            ('state', '=', 'posted'),
                            ], order=[('create_date', 'DESC')])
                    if not posted_transactions:
                        transaction, = transaction.copy([transaction])
                        transaction.provider_reference = (
                            charge['payment_intent'])
                transaction.charge_id = charge['id']
                transaction.save()
                transaction.safe_post()
                TransactionLog.create([{
                    'transaction': transaction.id,
                    'log': str(payload),
                }])
        return bool(transactions)

    @classmethod
    def webhook_charge_captured(cls, payload):
        return cls.webhook_charge_succeeded(payload, _event='charge.captured')

    @classmethod
    def webhook_charge_pending(cls, payload):
        return cls.webhook_charge_succeeded(payload, _event='charge.pending')

    @classmethod
    def webhook_charge_refunded(cls, payload):
        return cls.webhook_charge_succeeded(payload, _event='charge.pending')

    @classmethod
    def webhook_charge_failed(cls, payload, _event='charge.failed'):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')

        charge = payload['object']
        transactions = PaymentTransaction.search([
                ('provider_reference', '=', charge['payment_intent']),
                ('state', '!=', 'posted'),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error("%s: No Transactions for Payment Intent '%s'", _event,
                charge['payment_intent'])
        elif len(transactions) > 1:
            logger.error("%s: Multiple Transactions for Payment Intent '%s'",
                _event, charge['payment_intent'])
        for transaction in transactions:
            with Transaction().set_context(company=transaction.company.id):
                transaction.charge_id = charge['id']
                transaction.state = 'failed'
                transaction.save()
                transaction.delete_move_if_exists()
                TransactionLog.create([{
                    'transaction': transaction.id,
                    'log': str(payload),
                }])
        return bool(transactions)

    @classmethod
    def webhook_charge_dispute_created(cls, payload):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')

        source = payload['object']
        transactions = PaymentTransaction.search([
                ('charge_id', '=', source['charge']),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error(
                "charge.dispute.created: No Transaction for Charge '%s'",
                source['charge'])
        elif len(transactions) > 1:
            logger.error("charge.dispute.created: Multiple Transactions for Charge '%s'",
                source['charge'])
        for transaction in transactions:
            with Transaction().set_context(company=transaction.company.id):
                transaction.dispute_reason = source['reason']
                transaction.dispute_status = source['status']
                transaction.save()
                TransactionLog.create([{
                    'transaction': transaction.id,
                    'log': str(payload),
                }])
        return bool(transactions)

    @classmethod
    def webhook_charge_dispute_closed(cls, payload):
        pool = Pool()
        PaymentTransaction = pool.get('payment_gateway.transaction')
        TransactionLog = pool.get('payment_gateway.transaction.log')

        source = payload['object']
        transactions = PaymentTransaction.search([
                ('charge_id', '=', source['charge']),
                ], order=[('create_date', 'DESC')])
        if not transactions:
            logger.error(
                "charge.dispute.closed: No Transaction for Charge '%s'",
                source['charge'])
        elif len(transactions) > 1:
            logger.error("charge.dispute.closed: Multiple Transactions for Charge '%s'",
                source['charge'])
        for transaction in transactions:
            with Transaction().set_context(company=transaction.company.id):
                transaction.dispute_reason = source['reason']
                transaction.dispute_status = source['status']
                if source['status'] == 'lost':
                    if transaction.stripe_amount != source['amount']:
                        transaction.stripe_amount -= source['amount']
                    else:
                        transaction.state = 'failed'
                transaction.save()

                TransactionLog.create([{
                    'transaction': transaction.id,
                    'log': str(payload),
                }])
        return bool(transactions)

    #@classmethod
    #def webhook_source_chargeable(cls, payload):
    #    pool = Pool()
    #    Payment = pool.get('account.payment')

    #    source = payload['object']
    #    payments = Payment.search([
    #            ('stripe_token', '=', source['id']),
    #            ])
    #    if payments:
    #        Payment.write(payments, {'stripe_chargeable': True})
    #    return True

    #@classmethod
    #def webhook_source_failed(cls, payload):
    #    pool = Pool()
    #    Payment = pool.get('account.payment')

    #    source = payload['object']
    #    payments = Payment.search([
    #            ('stripe_token', '=', source['id']),
    #            ])
    #    for payment in payments:
    #        # TODO: remove when https://bugs.tryton.org/issue4080
    #        with Transaction().set_context(company=payment.company.id):
    #            Payment.fail([payment])
    #    return True

    #@classmethod
    #def webhook_source_canceled(cls, payload):
    #    pool = Pool()
    #    Payment = pool.get('account.payment')

    #    source = payload['object']
    #    payments = Payment.search([
    #            ('stripe_token', '=', source['id']),
    #            ])
    #    for payment in payments:
    #        # TODO: remove when https://bugs.tryton.org/issue4080
    #        with Transaction().set_context(company=payment.company.id):
    #            Payment.fail([payment])
    #    return True

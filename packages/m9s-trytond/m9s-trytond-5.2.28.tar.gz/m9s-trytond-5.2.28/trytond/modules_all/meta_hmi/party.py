# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import requests

import xml.etree.ElementTree as ET
from wtforms import IntegerField, BooleanField, StringField, ValidationError
from werkzeug.utils import redirect
from nereid import request, url_for, render_template, login_required, route, \
    current_user, flash, abort

from trytond.model import fields
from trytond.pool import PoolMeta, Pool
from trytond.exceptions import UserError
from trytond.modules.nereid.party import AddressForm
from trytond.modules.party.exceptions import InvalidIdentifierCode
from trytond.i18n import gettext

from nereid.contrib.locale import make_lazy_gettext
from nereid import current_app

_ = make_lazy_gettext('meta_hmi')


class CustomWebshopAddressForm(AddressForm):
    '''
    Custom address form
    Based directly on nereid.party/AddressForm to avoid the super on
    nereid_webshop.party/WebshopForm
      - overriding the subdivision field to be not required
      - adding fields company and vat_id (#2912)
    '''
    location = StringField(_('Location'))
    subdivision = IntegerField(_('State/County'))
    phone = StringField(_('Phone'))
    use_shipment_address = BooleanField(
        _('Use shipping address as billing address')
        )
    company = BooleanField(_('Order as a company'))
    vat_id = StringField(_('Vat-ID (required if company in EU)'))

    def validate_vat_id(form, field):
        pool = Pool()
        Identifier = pool.get('party.identifier')
        identifier = Identifier(type='eu_vat', code=field.data)
        if not field.data:
            return
        try:
            identifier.check_code()
        except InvalidIdentifierCode:
            msg = gettext('meta_hmi.msg_invalid_code',
                type=identifier.type_string,
                code=identifier.code)
            raise ValidationError(msg)

    def get_default_country(self):
        """
        nereid_webshop/party
        Get the default country based on geoip data.
        - Provide a fallback to Germany as the general default
        """
        if not request.remote_addr:
            return None

        Country = Pool().get('country.country')
        try:
            current_app.logger.debug(
                "GeoIP lookup for remote address: %s" % request.remote_addr)
            url = 'http://api.geoiplookup.net'
            payload = {'query': request.remote_addr}
            r = requests.get(url, params=payload)
            geoip_code = 'DE'
            if r.status_code == 200:
                tree = ET.fromstring(r.content)
                for element in tree.iter('*'):
                    if element.tag == 'countrycode':
                        geoip_code = element.text
                        current_app.logger.debug(
                            "GeoIP result: %s" % geoip_code)
                        break
            country, = Country.search([
                    ('code', '=', geoip_code)
                    ])
        except ValueError:
            return None
        return country

    def __init__(self, formdata=None, **kwargs):

        # While choices can be assigned after the form is constructed, default
        # cannot be. The form's data is picked from the first available of
        # formdata and kwargs.
        # Once the data has been resolved, changing the default won't do
        # anything.
        default_country = self.get_default_country()
        if default_country:
            kwargs.setdefault('country', default_country.id)
        super(CustomWebshopAddressForm, self).__init__(
            formdata, **kwargs)


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    description = fields.Text('Description')
    reference_customer = fields.Char('Supplier reference code',
        help='Reference code for our company as customer of this party.')

    def manage_vat_code(self, code):
        '''
        #2912
        - Adds an identifier to the party if it does not exist.
        - Removes an identifier on empty code.

        :return:
            - The created or deleted identifier or the one which existed
            - None if there was no identifier to delete
        '''
        Identifier = Pool().get('party.identifier')

        if not code:
            identifiers = Identifier.search([
                    ('party', '=', self.id),
                    ('type', '=', 'eu_vat'),
                    ])
            if identifiers:
                Identifier.delete(identifiers)
        else:
            identifiers = Identifier.search([
                ('party', '=', self.id),
                ('type', '=', 'eu_vat'),
                ('code', '=', code),
            ])
            if not identifiers:
                try:
                    identifiers = Identifier.create([{
                        'party': self.id,
                        'type': 'eu_vat',
                        'code': code,
                    }])
                except UserError as e:
                    flash(e.message)
                    abort(redirect(request.referrer))
        return identifiers[0] if identifiers else None

    @classmethod
    def default_account_receivable(cls, **pattern):
        pool = Pool()
        Configuration = pool.get('account.configuration')
        config = Configuration(1)
        account = config.get_multivalue(
            'default_account_receivable', **pattern)
        return account and account.id

    @classmethod
    def default_account_payable(cls, **pattern):
        pool = Pool()
        Configuration = pool.get('account.configuration')
        config = Configuration(1)
        account = config.get_multivalue(
            'default_account_payable', **pattern)
        return account and account.id


class PartyReplace(metaclass=PoolMeta):
    __name__ = 'party.replace'

    @classmethod
    def post_process(cls, party):
        pool = Pool()
        ContactMechanism = pool.get('party.contact_mechanism')

        super().post_process(party)

        contact_mechanisms = ContactMechanism.search([
                ('party', '=', party.id),
                ('active', '=', True),
                ])
        to_deactivate = []
        ids = [c.id for c in contact_mechanisms]
        for contact_mechanism in contact_mechanisms:
            actual_id = contact_mechanism.id
            duplicates = ContactMechanism.search([
                    ('id', 'in', ids),
                    ('id', '!=', actual_id),
                    ('type', '=', contact_mechanism.type),
                    ('value', '=', contact_mechanism.value),
                    ])
            to_deactivate += duplicates
            if actual_id in ids:
                ids.remove(actual_id)
            for duplicate in duplicates:
                ids.remove(duplicate.id)
        if to_deactivate:
            ContactMechanism.write(to_deactivate,
                {'active': False})


class PartyErase(metaclass=PoolMeta):
    __name__ = 'party.erase'

    def to_erase(self, party_id):
        pool = Pool()
        Party = pool.get('party.party')

        to_erase = super(PartyErase, self).to_erase(party_id)
        to_erase += [
            (Party, [('id', '=', party_id)], True,
                ['description', 'reference_customer'],
                [None, None]),
            ]
        return to_erase


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'

    def get_rec_name(self, name):
        party = zip_city = country = ''
        if self.party_name:
            party += self.party_name
        else:
            party += self.party.rec_name
        if self.zip:
            zip_city += self.zip + ' '
        if self.city:
            zip_city += self.city
        if self.country:
            country = self.country.code
        return ', '.join([_f for _f in [
                    party,
                    zip_city,
                    self.street,
                    country] if _f])

    def get_full_address(self, name):
        '''
        party/adress

        - Return a simple format for local (german) addresses
        - Return a correct international address format
        according to
        https://www.deutschepost.de/de/b/briefe-ins-ausland/brief-beschriften.html
        '''
        zip_city = subdivision = country = ''
        if self.zip:
            zip_city += self.zip + ' '
        if self.country and self.country.code == 'DE':
            if self.city:
                zip_city += self.city
        else:
            if self.city:
                zip_city += self.city.upper()
            if self.subdivision:
                subdivision = self.subdivision.name.upper()
            if self.country:
                country = self.country.name.upper()
        return '\n'.join([_f for _f in [
                    self.party_full_name,
                    self.street,
                    self.name,
                    zip_city,
                    subdivision,
                    country] if _f])

    @classmethod
    def get_address_form(cls, address=None):
        '''
        Override to use our CustomWebshopAddressForm.
        '''
        def get_legal_form(party):
            party_type = party.party_type
            if party_type == 'organization':
                return 'true'
            else:
                return ''

        if address:
            form = CustomWebshopAddressForm(
                request.form,
                name=address.party_full_name,
                street=address.street,
                location=address.name,
                zip=address.zip,
                city=address.city,
                country=address.country and address.country.id,
                subdivision=address.subdivision and address.subdivision.id,
                email=address.party.email,
                phone=address.phone,
                company=get_legal_form(address.party),
                vat_id=(address.party.tax_identifier
                    and address.party.tax_identifier.code)
                )
        else:
            if current_user.is_anonymous:
                address_name = ''
                company = ''
                vat_id = ''
                use_shipment_address = 'true'
            else:
                address_name = current_user.name
                company = get_legal_form(current_user.party)
                vat_id = (current_user.party.tax_identifier
                    and current_user.party.tax_identifier.code)
                use_shipment_address = ''
            form = CustomWebshopAddressForm(
                request.form,
                name=address_name,
                company=company,
                vat_id=vat_id,
                use_shipment_address=use_shipment_address,
                )

        return form

    @classmethod
    @route("/create-address", methods=["GET", "POST"])
    @login_required
    def create_address(cls):
        '''
        Override of create_address
          - to handle 0 ids of subdivision
          - to implement vat_id and company setting (#2912)
        Beware:
            There are multiple incarnations of this function that don't call super.
            Depending on the super chain there can also be random results for
            the call to this function. This one is taken from nereid_checkout.
            Exists also in trytond_nereid.
        '''
        form = cls.get_address_form()

        if request.method == 'POST' and form.validate():
            party = current_user.party
            address, = cls.create([{
                'party_name': form.name.data,
                'street': form.street.data,
                'name': form.location.data,
                'zip': form.zip.data,
                'city': form.city.data,
                'country': form.country.data,
                'subdivision': (None if form.subdivision.data == 0 else
                        form.subdivision.data),
                'party': party.id,
            }])
            if form.email.data:
                party.add_contact_mechanism_if_not_exists(
                    'email', form.email.data
                )
            if form.phone.data:
                phone = party.add_contact_mechanism_if_not_exists(
                    'phone', form.phone.data
                )
                cls.write([address], {
                    'phone': form.phone.data
                })
            if form.vat_id.data:
                vat_code = party.manage_vat_code(form.vat_id.data)
            if form.company.data:
                party.party_type = 'organization'
            else:
                party.party_type = 'person'
            party.save()
            return redirect(url_for('party.address.view_address'))

        return render_template('address-add.jinja', form=form)

    @classmethod
    @route("/save-new-address", methods=["GET", "POST"])
    @route("/edit-address/<int:address>", methods=["GET", "POST"])
    @login_required
    def edit_address(cls, address=None):
        '''
        Override of edit_address
          - to handle 0 ids of subdivision
          - to implement vat_id and company setting (#2912)
        Beware:
            There are multiple incarnations of this function that don't call super.
            Depending on the super chain there can also be random results for
            the call to this function. This one is a merge from nereid_checkout
            and trytond_nereid.
        '''
        form = cls.get_address_form()

        if address not in (a.id for a in current_user.party.addresses):
            # Check if the address is in the list of addresses of the
            # current user's party
            abort(403)

        address = cls(address)

        if request.method == 'POST' and form.validate():
            party = current_user.party
            cls.write([address], {
                'party_name': form.name.data,
                'street': form.street.data,
                'name': form.location.data,
                'zip': form.zip.data,
                'city': form.city.data,
                'country': form.country.data,
                'subdivision': (None if form.subdivision.data == 0 else
                        form.subdivision.data),
                'phone': form.phone.data if form.phone.data else '',
            })
            if form.email.data:
                party.add_contact_mechanism_if_not_exists(
                    'email', form.email.data
                )
            if form.phone.data:
                party.add_contact_mechanism_if_not_exists(
                    'phone', form.phone.data
                )
            vat_code = party.manage_vat_code(form.vat_id.data)
            if form.company.data:
                party.party_type = 'organization'
            else:
                party.party_type = 'person'
            party.save()
            return redirect(url_for('party.address.view_address'))

        elif request.method == 'GET' and address:
            # Its an edit of existing address, prefill data
            form = cls.get_address_form(address)

        return render_template(
            'address-edit.jinja', form=form, address=address)

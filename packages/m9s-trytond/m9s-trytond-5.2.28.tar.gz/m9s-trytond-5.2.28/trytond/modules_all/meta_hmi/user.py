# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from nereid import request, url_for, render_template, flash, jsonify, route, \
    current_website, current_locale
from werkzeug.utils import redirect
from wtforms import StringField, validators

from trytond.modules.nereid.user import RegistrationForm
from trytond.transaction import Transaction
from trytond.pool import PoolMeta, Pool
from nereid.signals import registration

from trytond.res.user import PasswordError
from nereid.contrib.locale import make_lazy_gettext

_ = make_lazy_gettext('meta_hmi')


class User(metaclass=PoolMeta):
    __name__ = "res.user"

    def get_status_bar(self, name):
        status = super(User, self).get_status_bar(name)
        status += ' - %s' % (Transaction().database.name)
        return status


class PersonRegistrationForm(RegistrationForm):
    first_name = StringField(_('First Name'), [validators.DataRequired(), ])


registration_form = PersonRegistrationForm


class NereidUser(metaclass=PoolMeta):
    __name__ = "nereid.user"

    @staticmethod
    def get_registration_form():
        '''
        Return a custom registration form for use with party_type
        in the site
        '''
        registration_form = PersonRegistrationForm()
        return registration_form

    @classmethod
    @route("/registration", methods=["GET", "POST"])
    def registration(cls):
        '''
        Monkey patch from trytond_nereid/user.py because of missing
        extensibility:
            - adds first_name handling
            - set default language depending from website locale
        '''
        pool = Pool()
        Party = pool.get('party.party')
        ContactMechanism = pool.get('party.contact_mechanism')

        registration_form = cls.get_registration_form()

        if registration_form.validate_on_submit():
            emails = cls.search([
                ('email', '=', registration_form.email.data),
                ('company', '=', current_website.company.id),
            ])
            if emails:
                message = _(
                    'A registration already exists with this email. '
                    'Please contact customer care'
                )
                if request.is_xhr or request.is_json:
                    return jsonify(message=str(message)), 400
                else:
                    flash(message)
            else:
                party = Party()
                party.name = registration_form.name.data
                party.first_name = registration_form.first_name.data
                party.lang = current_locale.language
                party.addresses = []
                party.contact_mechanisms = [
                    ContactMechanism(
                        type='email',
                        value=registration_form.email.data
                        ),
                    ]
                party.save()
                full_name = ' '.join([registration_form.first_name.data,
                        registration_form.name.data])
                nereid_user = cls(**{
                    'party': party.id,
                    'name': full_name,
                    'email': registration_form.email.data,
                    'password': registration_form.password.data,
                    'company': current_website.company.id,
                }
                )
                # Catch exceptions raised by password validation
                try:
                    nereid_user.save()
                except PasswordError as e:
                    return cls.build_response(e,
                        render_template('registration.jinja',
                            form=registration_form), 400)
                registration.send(nereid_user)
                nereid_user.send_activation_email()
                message = _(
                    'Registration Complete. Check your email for activation'
                )
                if request.is_xhr or request.is_json:
                    return jsonify(message=str(message)), 201
                else:
                    flash(message)
                return redirect(
                    request.args.get('next', url_for('nereid.website.home'))
                )

        if registration_form.errors and (request.is_xhr or request.is_json):
            return jsonify({
                'message': str(_('Form has errors')),
                'errors': registration_form.errors,
            }), 400

        return render_template('registration.jinja', form=registration_form)

    @staticmethod
    def default_timezone():
        return 'Europe/Berlin'

# This file is part account_code_digits module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Configuration', 'ConfigurationDefaultAccount', 'AccountTemplate',
    'Account', 'CreateChartAccount', 'CreateChart', 'UpdateChartStart',
    'UpdateChart']


class Configuration(metaclass=PoolMeta):
    __name__ = 'account.configuration'

    default_account_code_digits = fields.MultiValue(fields.Integer(
        'Account Code Digits',
        help='Number of digits to be used for all non-view accounts.'))
    force_digits = fields.Boolean('Force Digits',
        help='If marked it won\'t be allowed to create a non-view account'
        ' with a diferent number of digits than the number used on the '
        'selected on the chart creation.')

    @classmethod
    def multivalue_model(cls, field):
        pool = Pool()
        if field == 'default_account_code_digits':
            return pool.get('account.configuration.default_account')
        return super(Configuration, cls).multivalue_model(field)


class ConfigurationDefaultAccount(metaclass=PoolMeta):
    __name__ = 'account.configuration.default_account'
    default_account_code_digits = fields.Integer(
        "Account Code Digits",
        domain=[
            'OR',
            ('default_account_code_digits', '>=', 0),
            ('default_account_code_digits', '=', None),
            ])


class AccountTemplate(metaclass=PoolMeta):
    __name__ = 'account.account.template'

    def _get_account_value(self, account=None):
        pool = Pool()
        Config = pool.get('account.configuration')
        config = Config(1)
        res = super(AccountTemplate, self)._get_account_value(account)
        config_digits = config.default_account_code_digits
        if (self.type and self.parent and config_digits is not None):
            digits = int(config_digits - len(res.get('code', self.code)))
            if '%' in res.get('code', self.code):
                res['code'] = res.get('code', self.code).replace(
                    '%', '0' * (digits + 1))
            else:
                res['code'] = res.get('code', self.code) + '0' * digits
        # Don't upgrade code if the correct digits value is computed
        if account and res.get('code', '') == account.code:
            del res['code']
        return res


class Account(metaclass=PoolMeta):
    __name__ = 'account.account'

    @classmethod
    def validate(cls, accounts):
        pool = Pool()
        Config = pool.get('account.configuration')
        config = Config(1)
        super(Account, cls).validate(accounts)
        if config.default_account_code_digits and config.force_digits:
            for account in accounts:
                account.check_digits(config.default_account_code_digits)

    def check_digits(self, digits):
        # Only the first item of code is checked: "570000 (1)" -> "570000"
        code = self.code.split(' ')[0]
        if self.type and self.parent and len(code) != digits:
            raise UserError(gettext(
                'account_code_digits.invalid_code_digits',
                    account_digits=len(code),
                    account=self.rec_name,
                    digits=digits))

class CreateChartAccount(metaclass=PoolMeta):
    __name__ = 'account.create_chart.account'

    account_code_digits = fields.Integer('Account Code Digits',
        help='Number of digits to be used for all non-view accounts.')

    @classmethod
    def default_account_code_digits(cls):
        pool = Pool()
        Config = pool.get('account.configuration')
        config = Config(1)
        return config.default_account_code_digits


class CreateChart(metaclass=PoolMeta):
    __name__ = 'account.create_chart'

    def transition_create_account(self):
        pool = Pool()
        Config = pool.get('account.configuration')
        if hasattr(self.account, 'account_code_digits'):
            config = Config(1)
            config.default_account_code_digits = (
                self.account.account_code_digits)
            config.save()
        return super(CreateChart, self).transition_create_account()


class UpdateChartStart(metaclass=PoolMeta):
    __name__ = 'account.update_chart.start'

    account_code_digits = fields.Integer('Account Code Digits',
        help='Number of digits to be used for all non-view accounts.')

    @classmethod
    def default_account_code_digits(cls):
        pool = Pool()
        Config = pool.get('account.configuration')
        config = Config(1)
        return config.default_account_code_digits


class UpdateChart(metaclass=PoolMeta):
    __name__ = 'account.update_chart'

    def transition_update(self):
        pool = Pool()
        Config = pool.get('account.configuration')
        config = Config(1)
        config.default_account_code_digits = self.start.account_code_digits
        config.save()
        return super(UpdateChart, self).transition_update()

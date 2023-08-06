# This file is part of the account_code_digits module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
from trytond.pool import Pool
import trytond.tests.test_tryton
from trytond.exceptions import UserError
from trytond.tests.test_tryton import ModuleTestCase, with_transaction

from trytond.modules.company.tests import create_company, set_company
from trytond.modules.account.tests import create_chart


class AccountCodeDigitsTestCase(ModuleTestCase):
    'Test Account Code Digits module'
    module = 'account_code_digits'

    @with_transaction()
    def test_force_digits(self):
        'Test force digits'
        pool = Pool()
        Account = pool.get('account.account')
        Config = pool.get('account.configuration')
        company = create_company()
        with set_company(company):
            create_chart(company, tax=False)
            config = Config.get_singleton() or Config()
            config.default_account_code_digits = 6
            config.force_digits = True
            config.save()

            view = Account()
            view.name = 'view'
            view.code = '0'
            view.save()
            non_view, = Account.search([
                    ('type', '!=', 'None'),
                    ], limit=1)

            self.assertRaises(UserError, Account.write, [non_view],
                {'code': '000'})
            Account.write([view], {'code': '0'})
            Account.write([non_view], {'code': '000000'})
            self.assertEqual(view.code, '0')
            self.assertEqual(non_view.code, '000000')
            config.force_digits = False
            config.save()
            Account.write([non_view], {'code': '0000'})
            self.assertEqual(non_view.code, '0000')


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
            AccountCodeDigitsTestCase))
    return suite

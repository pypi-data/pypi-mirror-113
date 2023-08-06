# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.modules.jasper_reports.jasper import JasperReport
from .number_format import number_to_literal, SUPPORTED_LANGS

__all__ = ['Payment', 'Receipt']


class Payment(metaclass=PoolMeta):
    __name__ = 'account.payment'

    amount_literal = fields.Function(fields.Char('Amount Literal'),
        'get_amount_literal')

    def get_amount_literal(self, name):
        lang_code = None
        if self.party and self.party.lang:
            lang_code = self.party.lang.code
        if not lang_code or lang_code not in SUPPORTED_LANGS:
            lang_code = 'en'
        return number_to_literal(self.amount, lang_code)


class Receipt(JasperReport):
    __name__ = 'account.payment.receipt'

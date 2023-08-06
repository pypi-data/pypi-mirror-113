# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import If, Eval
from trytond.modules.party.party import STATES, DEPENDS

__all__ = ['Party', 'Invoice', 'InvoiceLine', 'Sale']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    customer = fields.Boolean('Customer', states=STATES, depends=DEPENDS)


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
        customer_domain = [If(Eval('type') == 'out',
                ('customer', '=', True),
                (),
                )]
        cls.party.domain.append(customer_domain)
        cls.party.depends.append('type')


class InvoiceLine(metaclass=PoolMeta):
    __name__ = 'account.invoice.line'

    @classmethod
    def __setup__(cls):
        super(InvoiceLine, cls).__setup__()
        customer_domain = [If(Eval('invoice_type') == 'out',
                ('customer', '=', True),
                (),
                )]
        cls.party.domain.append(customer_domain)
        cls.party.depends.append('invoice_type')


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'

    @classmethod
    def __setup__(cls):
        super(Sale, cls).__setup__()
        customer_domain = [('customer', '=', True)]
        if customer_domain not in cls.party.domain:
            cls.party.domain.append(customer_domain)

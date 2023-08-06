# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.modules.party.party import STATES, DEPENDS

__all__ = ['Party', 'Invoice', 'Sale', 'Purchase']


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'

    validated = fields.Boolean('Validated', states=STATES, depends=DEPENDS)


class PartyValidatedMixin(metaclass=PoolMeta):
    @classmethod
    def __setup__(cls):
        super(PartyValidatedMixin, cls).__setup__()
        cls.party.domain.append(('validated', '=', True))


class Invoice(PartyValidatedMixin, metaclass=PoolMeta):
    __name__ = 'account.invoice'


class Sale(PartyValidatedMixin, metaclass=PoolMeta):
    __name__ = 'sale.sale'


class Purchase(PartyValidatedMixin, metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

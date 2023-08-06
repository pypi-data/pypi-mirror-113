# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.modules.product.product import STATES, DEPENDS

__all__ = ['Template', 'InvoiceLine', 'SaleLine', 'PurchaseLine']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    validated = fields.Boolean('Validated', states=STATES, depends=DEPENDS)


class ProductValidatedMixin(object):
    @classmethod
    def __setup__(cls):
        super(ProductValidatedMixin, cls).__setup__()
        cls.product.domain.append(('template.validated', '=', True))


class InvoiceLine(ProductValidatedMixin, metaclass=PoolMeta):
    __name__ = 'account.invoice.line'


class SaleLine(ProductValidatedMixin, metaclass=PoolMeta):
    __name__ = 'sale.line'


class PurchaseLine(ProductValidatedMixin, metaclass=PoolMeta):
    __name__ = 'purchase.line'

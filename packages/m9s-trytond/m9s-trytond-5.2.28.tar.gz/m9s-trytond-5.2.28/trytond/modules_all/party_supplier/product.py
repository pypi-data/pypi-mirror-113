# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['ProductSupplier']


class ProductSupplier(metaclass=PoolMeta):
    __name__ = 'purchase.product_supplier'

    @classmethod
    def __setup__(cls):
        super(ProductSupplier, cls).__setup__()
        new_domain = ('supplier', '=', True)
        domain = cls.party.domain[:]
        if domain and new_domain not in domain:
            cls.party.domain.extend(new_domain)
        else:
            cls.party.domain = [new_domain]

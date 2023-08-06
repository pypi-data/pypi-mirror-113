# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta


class Payment(metaclass=PoolMeta):
    __name__ = 'sale.payment'

    def get_payment_description(self, name):
        """
        Return a short description of the sale payment
        This can be used in documents to show payment details
        """
        description = u'Überweisung'
        if (self.method == 'manual'
                and description in self.gateway.name):
            return description
        return super().get_payment_description(name)

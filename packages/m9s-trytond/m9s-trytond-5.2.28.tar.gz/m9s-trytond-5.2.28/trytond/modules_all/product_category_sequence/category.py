# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import sequence_ordered

__all__ = ['Category']


class Category(sequence_ordered(), metaclass=PoolMeta):
    __name__ = 'product.category'

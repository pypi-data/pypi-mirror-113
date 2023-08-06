# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import Pool
from . import res


def register():
    Pool.register(
        res.User,
        module='authentication_none', type_='model')

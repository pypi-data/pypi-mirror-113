#This file is part party_search module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.

from trytond.pool import Pool
from . import party
from . import address


def register():
    Pool.register(
        party.Party,
        address.Address,
        module='party_search', type_='model')

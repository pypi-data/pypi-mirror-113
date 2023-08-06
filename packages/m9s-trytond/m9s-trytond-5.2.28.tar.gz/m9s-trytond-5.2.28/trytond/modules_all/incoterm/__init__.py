# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import incoterm
from . import party


def register():
    Pool.register(
        incoterm.Category,
        incoterm.Incoterm,
        party.Party,
        party.PartyIncoterm,
        module='incoterm', type_='model')

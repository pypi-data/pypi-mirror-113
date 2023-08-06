# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from .party import *


def register():
    Pool.register(
        Iae,
        Party,
        PartyIae,
        module='party_iae', type_='model')

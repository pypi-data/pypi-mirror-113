#This file is part party_asterisk module for Tryton.
#The COPYRIGHT file at the top level of this repository contains
#the full copyright notices and license terms.
from trytond.pool import Pool
from .contact_mechanism import *

def register():
    Pool.register(
        ContactMechanism,
        module='party_asterisk', type_='model')

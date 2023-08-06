# This file is part activity_category module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import activity

def register():
    Pool.register(
        activity.Category,
        activity.Activity,
        activity.ActivityCategory,
        module='activity_category', type_='model')

# This file is part purchase_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import purchase


def register():
    Pool.register(
        purchase.PurchaseReport,
        purchase.PurchaseRequestReport,
        module='purchase_jreport', type_='report')

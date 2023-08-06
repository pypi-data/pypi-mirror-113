# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool

from . import asset


def register():
    Pool.register(
        asset.Asset,
        asset.AnalyticAccountEntry,
        module='analytic_asset', type_='model')

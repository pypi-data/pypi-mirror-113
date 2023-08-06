# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import bom


def register():
    Pool.register(
        bom.BOM,
        bom.ProductionBomOrcad,
        module='production_bom_orcad_import', type_='model')

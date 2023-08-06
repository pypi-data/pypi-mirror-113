# This file is part of stock_move_jasper module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.modules.jasper_reports.jasper import JasperReport
from trytond.pool import PoolMeta

__all__ = ['MoveReport']
__metaclass__ = PoolMeta


class MoveReport(JasperReport):
    __name__ = 'stock.move.jreport'

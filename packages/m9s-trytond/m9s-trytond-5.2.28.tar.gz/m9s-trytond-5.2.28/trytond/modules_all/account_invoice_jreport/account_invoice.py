# This file is part account_invoice_jreport module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.modules.jasper_reports.jasper import JasperReport
from trytond.config import config as config_

POST_INVOICE = config_.getboolean('jasper', 'post_invoice', default=True)

__all__ = ['Invoice', 'InvoiceReport']


class InvoiceReport(JasperReport, metaclass=PoolMeta):
    __name__ = 'account.invoice.jreport'


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    def print_invoice(self):
        if POST_INVOICE:
            super(Invoice, self).print_invoice()
        else:
            pass

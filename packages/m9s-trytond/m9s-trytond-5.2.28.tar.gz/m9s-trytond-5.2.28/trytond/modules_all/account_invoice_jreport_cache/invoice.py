# -*- encoding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool, PoolMeta
from trytond.modules.jasper_reports.jasper import JasperReport
from trytond.exceptions import UserError
from trytond.rpc import RPC

__all__ = ['Invoice', 'InvoiceReport']


class Invoice(metaclass=PoolMeta):
    __name__ = 'account.invoice'

    def print_invoice(self):
        '''
        Generate invoice report and store it in invoice_report field.
        '''
        if self.invoice_report_cache:
            return
        InvoiceReport = Pool().get('account.invoice.jreport', type='report')
        InvoiceReport.execute([self.id], {})


class InvoiceReport(JasperReport):
    __name__ = 'account.invoice.jreport'

    @classmethod
    def __setup__(cls):
        super(InvoiceReport, cls).__setup__()
        cls.__rpc__['execute'] = RPC(False)

    @classmethod
    def render(cls, report, data, model, ids):
        pool = Pool()
        Invoice = pool.get('account.invoice')

        new_invoices = []
        invoice_reports_cache = []
        invoice_reports_format = []
        for invoice in Invoice.browse(ids):
            if invoice.invoice_report_cache:
                invoice_reports_cache.append(invoice.invoice_report_cache)
                invoice_reports_format.append(invoice.invoice_report_format)
            else:
                new_invoices.append(invoice.id)
        pages = len(invoice_reports_cache) or 1

        invoice_reports_format = list(set(invoice_reports_format))

        if invoice_reports_format and len(invoice_reports_format) != 1:
            raise UserError('Warning', 'When try to generate multiple '
                'reports at same time all them need to be the same format.'
                ' E.g.: "pdf".')

        invoice_reports_format = (invoice_reports_format and
            invoice_reports_format[0] or '')
        if invoice_reports_cache and invoice_reports_format == 'pdf':
            ndata = None
            if new_invoices:
                ntype, ndata, npages = super(InvoiceReport, cls).render(
                    report, data, model, new_invoices)
            if ndata:
                invoice_reports_cache.append(ndata)
                pages = pages + npages
            file_data = JasperReport.merge_pdfs(invoice_reports_cache)
            return (invoice_reports_format, file_data, pages)

        res = super(InvoiceReport, cls).render(report, data, model, ids)

        if len(ids) == 1:
            invoice = Invoice(ids[0])
            if invoice.state in ('posted', 'paid') and invoice.type == 'out':
                invoice.invoice_report_format = res[0]
                invoice.invoice_report_cache = res[1]
                invoice.save()
        return res

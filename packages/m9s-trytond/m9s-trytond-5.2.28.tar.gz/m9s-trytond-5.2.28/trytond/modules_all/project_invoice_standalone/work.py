# This file is part project_invoice_description module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction
from itertools import groupby
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Work']


class Work(metaclass=PoolMeta):
    __name__ = 'project.work'
    invoice_standalone = fields.Boolean('Invoice Lines',
        states={
            'invisible': ((Eval('invoice_method') == 'manual')
                | (Eval('type') != 'project')),
            },
        depends=['invoice_method', 'type'],
        help='Create invoice lines according to the invoice method')

    @classmethod
    @ModelView.button
    def invoice(cls, works):
        '''Create invoice or invoice lines'''
        pool = Pool()
        Invoice = pool.get('account.invoice')

        for work in works:
            if work.invoice_standalone:  # create invoice lines
                if not work.party:
                    raise UserError(gettext('project_invoice.msg_missing_party',
                        work=work.rec_name))

                invoice_lines, uninvoiced_children = work._get_lines_to_invoice()
                if not invoice_lines:
                    continue
                for key, lines in groupby(invoice_lines,
                        key=work._group_lines_to_invoice_key):
                    lines = list(lines)
                    key = dict(key)

                    with Transaction().set_context({
                            'invoice_type': 'out',
                            'standalone': True,
                            }):
                        invoice = Invoice()
                        invoice.party = work.party

                        invoice_line = work._get_invoice_line(key, invoice, lines)
                        invoice_line.invoice_type = 'out'
                        invoice_line.party = work.party
                        invoice_line.save()

                    origins = {}
                    for line in lines:
                        origin = line['origin']
                        origins.setdefault(origin.__class__, []).append(origin)
                    for klass, records in origins.items():
                        klass.write(records, {
                                'invoice_line': invoice_line.id,
                                })
            else:  # create invoice + lines
                super(Work, cls).invoice(works)

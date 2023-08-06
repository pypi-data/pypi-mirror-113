# This file is part account_payment_gateway_invoice module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool, PoolMeta

from trytond.transaction import Transaction


__all__ = ['AccountPaymentGatewayTransaction']


class AccountPaymentGatewayTransaction(metaclass=PoolMeta):
    __name__ = 'account.payment.gateway.transaction'

    @classmethod
    def _get_origin(cls):
        res = super(AccountPaymentGatewayTransaction, cls)._get_origin()
        res.append('account.invoice')
        return res

    def pay_invoice(self, invoice):
        pool = Pool()
        Invoice = pool.get('account.invoice')
        PaymentMethod = pool.get('account.invoice.payment.method')
        PayInvoice = pool.get('account.invoice.pay', type='wizard')

        payment_method = PaymentMethod.search([
                ('name', '=', self.gateway.journal.name),
                ])
        Invoice.workflow_to_posted([invoice])
        if not invoice.amount_to_pay:
            return
        with Transaction().set_context({'active_id': invoice.id}):
            session_id, _, _ = PayInvoice.create()
            pay_invoice = PayInvoice(session_id)
            pay_invoice.start.currency = self.currency
            pay_invoice.start.currency_digits = (self
                .currency_digits)
            pay_invoice.start.description = self.description
            pay_invoice.start.payment_method = payment_method[0]
            pay_invoice.start.date = self.date
            pay_invoice.start.amount = self.amount
            if invoice.total_amount != self.amount:
                min_percent_writeoff = invoice.total_amount * (1 -
                    self.gateway.writeoff_amount_percent)
                max_percent_writeoff = invoice.total_amount * (1 +
                    self.gateway.writeoff_amount_percent)
                [setattr(pay_invoice.ask, f, v)
                    for f, v in pay_invoice.default_ask(None)
                    .iteritems()]

                if (min_percent_writeoff < self.amount <
                        max_percent_writeoff
                        or self.amount > invoice.amount_to_pay):
                    pay_invoice.ask.type = 'writeoff'
                    pay_invoice.ask.journal_writeoff = (self
                        .gateway.journal_writeoff)
                else:
                    pay_invoice.ask.type = 'partial'
            pay_invoice.transition_pay()
            PayInvoice.delete(session_id)

    @classmethod
    def pay_invoices(cls, transactions):
        for transaction in transactions:
            invoice = transaction.origin
            transaction.pay_invoice(invoice)

    @classmethod
    def confirm(cls, transactions):
        Invoice = Pool().get('account.invoice')

        transactions = [t for t in transactions
            if isinstance(t.origin, Invoice)]
        cls.pay_invoices(transactions)

        super(AccountPaymentGatewayTransaction, cls).confirm(transactions)

    @classmethod
    def refund(cls, transactions):
        Invoice = Pool().get('account.invoice')

        transactions = [t for t in transactions
            if isinstance(t.origin, Invoice)]
        cls.pay_invoices(transactions)

        for transaction in transactions:
            invoice = transaction.origin
            if invoice.state == 'paid':
                # TODO: Pending to test if credit invoice is already
                # created before create a new one
                credit, = Invoice.credit([invoice])

                # TODO: delete this line when you have developed the refund
                # transaction through the payment gateway
                transaction.pay_invoice(credit)

        super(AccountPaymentGatewayTransaction, cls).refund(transactions)

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import batch
from . import carrier
from . import channel
from . import checkout
from . import cms
from . import configuration
from . import contract
from . import gift_card
from . import import_rule
from . import index
from . import inventory
from . import invoice
from . import ir
from . import order_point
from . import party
from . import payment
from . import product
from . import purchase
from . import purchase_request
from . import report
from . import sale
from . import shipment
from . import stock
from . import transaction
from . import tree
from . import user
from . import website

__all__ = ['register']


def register():
    Pool.register(
        batch.BatchLine,
        carrier.Carrier,
        channel.SaleChannel,
        checkout.Cart,
        checkout.Checkout,
        cms.Article,
        cms.MenuItem,
        configuration.Configuration,
        contract.Contract,
        gift_card.GiftCard,
        index.IndexBacklog,
        inventory.Inventory,
        invoice.Invoice,
        invoice.InvoiceLine,
        import_rule.BankingImportRuleInformation,
        ir.Cron,
        order_point.OrderPoint,
        party.Party,
        party.Address,
        payment.Payment,
        product.Category,
        product.CategoryAccount,
        product.Product,
        product.ProductSupplier,
        product.Template,
        purchase.PurchaseLine,
        purchase_request.PurchaseRequest,
        sale.Sale,
        sale.SaleLine,
        shipment.ShipmentIn,
        shipment.ShipmentOut,
        stock.CreateSaleShippingStart,
        stock.Package,
        transaction.PaymentGateway,
        transaction.PaymentTransaction,
        tree.Node,
        user.NereidUser,
        user.User,
        website.Website,
        module='meta_hmi', type_='model')
    Pool.register(
        party.PartyErase,
        party.PartyReplace,
        sale.AddSalePayment,
        stock.CreateSaleShipping,
        module='meta_hmi', type_='wizard')
    Pool.register(
        report.DeliveryNote,
        report.InvoiceReport,
        report.PurchaseReport,
        report.PurchaseReportHmiWoPrices,
        report.SaleReport,
        report.TrialBalance,
        module='meta_hmi', type_='report')

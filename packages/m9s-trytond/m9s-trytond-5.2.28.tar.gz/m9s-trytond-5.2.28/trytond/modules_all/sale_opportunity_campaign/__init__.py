# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
from . import opportunity
from . import invoice

def register():
    Pool.register(
        opportunity.Source,
        opportunity.Campaign,
        opportunity.ProductCampaign,
        opportunity.PartyCampaign,
        opportunity.Opportunity,
        opportunity.CreateCampaignStart,
        invoice.InvoiceLine,
        module='sale_opportunity_campaign', type_='model')
    Pool.register(
        opportunity.CreateCampaign,
        module='sale_opportunity_campaign', type_='wizard')

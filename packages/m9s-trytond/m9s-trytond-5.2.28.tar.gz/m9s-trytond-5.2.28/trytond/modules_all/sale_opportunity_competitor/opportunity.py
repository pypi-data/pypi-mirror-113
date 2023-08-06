from trytond.model import ModelSQL, ModelView, fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Template', 'Party', 'ProductCompetitor', 'Competitor',
    'Opportunity']


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    strengths = fields.Text('Strengths')
    weaknesses = fields.Text('Weaknesses')
    opportunities = fields.Text('Opportunities')
    threats = fields.Text('Threats')
    competitors = fields.One2Many('product.competitor', 'product',
        'Competitors')


class Party(metaclass=PoolMeta):
    __name__ = 'party.party'
    competitor = fields.Boolean('Competitor')
    strengths = fields.Text('Strengths')
    weaknesses = fields.Text('Weaknesses')
    opportunities = fields.Text('Opportunities')
    threats = fields.Text('Threats')

    @classmethod
    def view_attributes(cls):
        return super(Party, cls).view_attributes() + [
            ('//page[@id="swot"]', 'states', {
                    'invisible': ~Eval('competitor', False),
                    })]


class ProductCompetitor(ModelSQL, ModelView):
    'Product Competitor'
    __name__ = 'product.competitor'
    party = fields.Many2One('party.party', 'Party', required=True, domain=[
            ('competitor', '=', True),
            ])
    product = fields.Many2One('product.template', 'Product', required=True)
    strengths = fields.Text('Strengths')
    weaknesses = fields.Text('Weaknesses')
    opportunities = fields.Text('Opportunities')
    threats = fields.Text('Threats')

    def get_rec_name(self, name):
        return '%s - %s' % (self.product.name, self.party.rec_name)


class Competitor(ModelSQL, ModelView):
    'Sale Opportunity Competitor'
    __name__ = 'sale.opportunity.competitor'
    opportunity = fields.Many2One('sale.opportunity', 'Opportunity',
        required=True)
    party = fields.Many2One('party.party', 'Party', domain=[
            ('competitor', '=', True),
            ])
    product = fields.Many2One('product.product', 'Product')
    competitor = fields.Function(fields.Many2One('product.competitor',
            'Competitor'), 'get_competitor')
    notes = fields.Text('Notes')
    state = fields.Selection([
            ('competing', 'Competing'),
            ('won', 'Won'),
            ('lost', 'Lost'),
            ], 'State', required=True)

    @staticmethod
    def default_state():
        return 'competing'

    def get_competitor(self, name):
        if not self.party or not self.product:
            return
        for competitor in self.product.template.competitors:
            if competitor.party == self.party:
                return competitor.id


class Opportunity(metaclass=PoolMeta):
    __name__ = 'sale.opportunity'
    competitors = fields.One2Many('sale.opportunity.competitor', 'opportunity',
        'Competitors')

# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import PoolMeta
from trytond.modules.account_invoice_contact.invoice import ContactMixin

__all__ = ['ConfigurationRelationType', 'Configuration', 'Sale']


class ConfigurationRelationType(ModelSQL):
    'Sale Configuration - Party relation type'
    __name__ = 'sale.configuration-party.relation.type'

    relation = fields.Many2One('party.relation.type', 'Relation Type',
        required=True, select=True)
    config = fields.Many2One('sale.configuration', 'Config',
        required=True, select=True)


class Configuration(metaclass=PoolMeta):
    __name__ = 'sale.configuration'

    relation_types = fields.Many2Many(
        'sale.configuration-party.relation.type', 'config',
        'relation', 'Contact types')


class Sale(ContactMixin, metaclass=PoolMeta):
    __name__ = 'sale.sale'
    _contact_config_name = 'sale.configuration'

    def _get_invoice_sale(self):
        invoice = super(Sale, self)._get_invoice_sale()
        if self.contact:
            invoice.contact = self.contact
        return invoice

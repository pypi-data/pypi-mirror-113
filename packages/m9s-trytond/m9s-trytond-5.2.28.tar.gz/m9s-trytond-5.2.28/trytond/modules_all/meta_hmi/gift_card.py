# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import uuid

from trytond.model import fields, Workflow, ModelView
from trytond.pool import PoolMeta, Pool


class GiftCard(metaclass=PoolMeta):
    __name__ = 'gift_card.gift_card'

    def _get_subject_for_email(self):
        """
        Returns the text to use as subject of email
        """
        return "Gutschein - Nr.: %s" % self.number

    def _get_email_templates(self):
        '''
        gift_card/gift_card.py
        '''
        #return (
        #    'emails/gift_card_html.jinja',
        #    'emails/gift_card_text.jinja'
        #)
        from jinja2 import Environment, PackageLoader
        env = Environment(loader=PackageLoader(
            'trytond.modules.nereid_webshop', 'templates/emails'
        ))
        return (
            env.get_template('gift_card_html.jinja'),
            env.get_template('gift_card_text.jinja')
            )

    @classmethod
    def get_gift_card_number(cls):
        '''
        We add the first part of a uuid4 as unique identifier for the gift card
        '''
        sequence = super(GiftCard, cls).get_gift_card_number()
        number = str(uuid.uuid4()).split('-')[0]
        return '-'.join([number, sequence])

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import re
import requests

from datetime import datetime
from jinja2 import evalcontextfilter, Markup, escape

from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.transaction import Transaction
from trytond.config import config
from nereid import route, render_template, template_filter, cache, \
    current_website, current_locale
from nereid.helpers import key_from_list

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

sitemap_depth = config.getint('website', 'sitemap_depth', default=2)


class Website(metaclass=PoolMeta):
    __name__ = 'nereid.website'

    price_display = fields.Selection([
                ('no_tax', 'Net (B2B)'),
                ('with_tax', 'Tax included (B2C)'),
                ], 'Price display', required=True,
            help='How the prices on the website shall be displayed.'
            )
    home_article = fields.Many2One('nereid.cms.article', "Frontpage article",
        ondelete='RESTRICT', select=True)

    @staticmethod
    def default_price_display():
        return 'no_tax'

    @classmethod
    @route('/404', methods=["GET"])
    def render_404(cls):
        '''
        The 404 template extends nereid_webshop/templates/sitemap.jinja.
        '''
        sitemap = cls._get_sitemap()
        return render_template('404.jinja', sitemap=sitemap)

    @classmethod
    @route('/403', methods=["GET"])
    def render_403(cls):
        '''
        The 403 template extends nereid_webshop/templates/base.jinja.
        '''
        return render_template('403.jinja')

    @classmethod
    @template_filter()
    @evalcontextfilter
    def nl2br(cls, eval_ctx, value):
        '''
        Add the custom nl2br filter to the jinja environment
          - http://jinja.pocoo.org/docs/dev/api/#custom-filters
        '''
        result = '\n\n'.join('<p>%s</p>' % p.replace('\n', Markup('<br>\n'))
                              for p in _paragraph_re.split(escape(value)))
        if eval_ctx.autoescape:
            result = Markup(result)
        return result

    @classmethod
    @route('/sitemap', methods=["GET"])
    def render_sitemap(cls):
        '''
        nereid_webshop
         - Override with an implementation that takes into account
           sitemap_depth settings on nodes (s. tree.py)
        '''
        sitemap = cls._get_sitemap()
        return render_template('sitemap.jinja', sitemap=sitemap)

    @classmethod
    def _get_sitemap(cls):
        '''
         - Override with an implementation that takes into account
           sitemap_depth settings on nodes (s. tree.py)
        '''
        Node = Pool().get('product.tree_node')

        cache_key = key_from_list([
                Transaction().database.name,
                current_website.id,
                current_locale.id,
                sitemap_depth,
                'product.tree_node',
                ])
        if cls._get_sitemap_expiration():
            sitemap = None
            cache.delete(cache_key)
        else:
            sitemap = cache.get(cache_key)
        if sitemap is None:
            sitemap = {}
            base_nodes = Node.search([
                    ('parent', '=', None),
                    ], order=[
                    ('sequence', 'ASC'),
                    ])
            for node in base_nodes:
                node_depth = node.sitemap_depth or sitemap_depth
                # Do not display nodes with depth -1
                if node_depth >= 0:
                    sitemap.update(node.get_web_sitemap_item(depth=node_depth))
            # Set the cache for three days and force regeneration on specific
            # day times via cron job
            cache.set(cache_key, sitemap, 60 * 60 * 24 * 3)
        return sitemap

    @classmethod
    def _get_sitemap_expiration(cls):
        '''
        A helper method to check, if the sitemap has expired and should be
        refreshed.
        For simplicity we use here a hard coded time window of two hours
        in the night. Take care to update only once in that interval by
        creating a helper cache entry with timeout of 3h (#2934).
        '''
        update_key = key_from_list([
                Transaction().database.name,
                current_website.id,
                current_locale.id,
                sitemap_depth,
                'web_sitemap_update',
                ])
        last_update = cache.get(update_key)
        if last_update is None:
            begin = 1
            end = 2
            current_hour = datetime.utcnow().hour
            if (begin <= current_hour <= end):
                cache.set(update_key, True, 60 * 60 * 3)
                return True
        return False

    @classmethod
    def refresh_sitemap_cache(cls):
        '''
        cron job method to refresh the sitemap cache
        '''
        for site in cls.search([]):
            url = ('').join(['https://', site.name, '/de/sitemap'])
            r = requests.get(url)

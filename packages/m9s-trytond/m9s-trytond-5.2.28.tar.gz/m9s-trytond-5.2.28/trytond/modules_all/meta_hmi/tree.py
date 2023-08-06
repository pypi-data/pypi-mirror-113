# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta, Pool
from trytond.model import fields
from trytond.cache import Cache
from trytond.exceptions import UserError
from nereid import (Markup, route, request, abort, render_template,
    current_website)
from nereid.contrib.sitemap import SitemapIndex, SitemapSection


class Node(metaclass=PoolMeta):
    __name__ = "product.tree_node"

    default_image = fields.Function(
        fields.Many2One('nereid.static.file', 'Image'), 'get_default_image',
    )
    sitemap_depth = fields.Integer('Web sitemap depth',
        help='Define how many children levels shall be displayed in the '
        'web sitemap:\n'
        'empty: Use the default\n'
        '-1: Do not display\n'
        '0: Display just this entry\n'
        '>=1: Use this level of children')

    @classmethod
    def get_template(cls):
        res = super(Node, cls).get_template()
        res.extend([
            ('catalog/final-node.html', 'Final Node'),
            ('catalog/category.html', 'Category'),
            ])
        return res

    def get_default_image(self, name=None):
        '''
        Iterate all parent nodes until we get a default image
        '''
        if self.image:
            return self.image.id
        parent_image = self.get_parent_image()
        if parent_image:
            return parent_image.id
        image = current_website.default_product_image
        return image and image.id or None

    def get_parent_image(self):
        if self.parent:
            if self.parent.image:
                return self.parent.image
            else:
                return self.parent.get_parent_image()
        return None

    @staticmethod
    def default_products_per_page():
        return 25

    @route('/nodes/<int:active_id>/<slug>/<int:page>')
    @route('/nodes/<int:active_id>/<slug>')
    def render(self, slug=None, page=1):
        '''
        nereid_catalog_tree:
            Complete override to provide canonical_url (#3375)
        '''
        if not self.slug or not self.active:
            abort(404)

        if self.type_ != 'catalog':
            # Display only catalog nodes
            abort(403)

        products = self.get_products(
            page=page, per_page=self.products_per_page)

        canonical_url = request.base_url
        return render_template(
            self.template, products=products, node=self,
            canonical_url=canonical_url)

    '''
    Set a cache for node menuitems to speedup the menu creation
    '''
    _node_menuitem_cache = Cache('product.tree_node', context=False)

    @classmethod
    def clear_node_menuitem_cache(cls, *args):
        '''
        A method which conveniently clears the cache
         - used in triggers
        '''
        cls._node_menuitem_cache.clear()

    def get_menu_item(self, max_depth):
        cache_rv = self._node_menuitem_cache.get(self.id)
        if cache_rv is not None:
            return cache_rv
        res = super(Node, self).get_menu_item(max_depth)
        self._node_menuitem_cache.set(self.id, res)
        return res

    def get_meta_description(self):
        '''
        Provide a useful description for the meta description tag
        https://support.google.com/webmasters/answer/79812?hl=en&ref_topic=4617741
        https://support.google.com/webmasters/answer/35624?rd=1#1
            <meta name="Description" CONTENT="Author: A.N. Author,
            Illustrator: P. Picture, Category: Books, Price:  £9.24,
            Length: 784 pages">
        '''
        description = 'Kategorie: %s' % self.rec_name
        if self.products:
            description += ', Produkte: ' + '; '.join(
                [p.product.name for p in self.products])
        elif self.children:
            description += ', Inhalt: ' + '; '.join(
                [p.name for p in self.children])
        return Markup(description)

    @classmethod
    @route('/sitemaps/tree-index.xml', defaults={'priority': 0.5})
    @route('/sitemaps/tree-index.xml/<priority>')
    def sitemap_index(cls, priority):
        '''
        Return a Sitemap Index Page with URLs suitable to parse the priority
        in the sections (see below)
        '''
        if priority == 'all':
            priority = 0.5
            # provide all priorities from get_priority_domain, that should
            # appear in the concatenated sitemap index
            priorities = [0.2, 0.3, 0.8, 1.0]
        else:
            priorities = priority = [priority]
        domain = cls.get_priority_domain(priority)
        index = SitemapIndex(cls, domain, priorities=priorities)
        return index.render()

    @classmethod
    @route('/sitemaps/tree-<int:page>.xml?priority=<priority>')
    def sitemap(cls, page, priority):
        domain = cls.get_priority_domain(priority)
        sitemap_section = SitemapSection(
            cls, domain, page)
        sitemap_section.changefreq = 'daily'
        sitemap_section.priority = priority
        return sitemap_section.render()

    @classmethod
    def get_priority_domain(cls, priority):
        '''
        Implement here our custom strategy to prioritize high our important
        node groups.
        prio 0.5 = default all with prio 0.5

        Strategy:
            - basically we use the defined top level nodes and get their
              children
                - take care to use those nodes only once
                - take care to not use nodes pointing to duplicate content
        '''
        domain = [
                ('active', '=', True),
                ]
        node_slugs = None
        if priority == '1.0':
            node_slugs = ('saiten', 'zubehor')
        elif priority == '0.8':
            node_slugs = ('bags', 'etuis', 'geschenke')
        elif priority == '0.3':
            node_slugs = ('geigenbau', 'pyramid', 'winter', 'soundwear',
                'savarez_1')
        elif priority == '0.2':
            node_slugs = ('gewa', 'old', 'msa-schnerr')

        if node_slugs:
            nodes = cls.search([('slug', 'in', node_slugs)])
            or_domain = ['OR', ]
            for node in nodes:
                or_domain.append(('parent', 'child_of', node))
            domain.append(or_domain)
        return domain

    def get_web_sitemap_item(self, depth):
        '''
        Build a huge dict of sitemap node urls and their children.
          - Add the brand in front of the node name for better SEO
            representation
        '''
        ProductTreeNode = Pool().get('product.product-product.tree_node')

        sitemap = {}
        brand = ''
        product_nodes = ProductTreeNode.search([
                ('node', '=', self.id),
                ])
        if product_nodes:
            product = product_nodes[0].product
            brand = product.brand and product.brand.rec_name or ''
            brand += ' '
        node_name = ''.join([brand, self.name])
        sitemap.setdefault(node_name, {})
        sitemap[node_name].setdefault('children', {})
        sitemap[node_name]['url'] = self.get_absolute_url()
        node_depth = self.sitemap_depth or depth
        if node_depth > 0 and self.children:
            children = {}
            for child in self.children:
                children.update(child.get_web_sitemap_item(depth=node_depth - 1))
            sitemap[node_name]['children'] = children
        return sitemap

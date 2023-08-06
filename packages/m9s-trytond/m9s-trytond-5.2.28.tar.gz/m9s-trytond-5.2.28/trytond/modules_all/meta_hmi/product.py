# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import datetime

from decimal import Decimal
from functools import partial

from trytond.model import fields
from trytond.pyson import Eval
from trytond.pool import PoolMeta, Pool
from trytond.transaction import Transaction
from trytond.modules.product import price_digits
from trytond.cache import Cache

from nereid import (
    current_user, request, Markup, route, current_locale, current_website)
from nereid.contrib.sitemap import SitemapIndex, SitemapSection

from pyes.filters import BoolFilter, ANDFilter, ORFilter, TermFilter
from pyes import BoolQuery, MatchQuery, NestedQuery
from babel import numbers

from nereid.contrib.locale import make_lazy_gettext

_ = make_lazy_gettext('meta_hmi')


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'

    @staticmethod
    def default_supply_on_sale():
        return True

    @staticmethod
    def default_weight_uom():
        '''
        product
            - preset our custom weight
        '''
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_gram')

    @staticmethod
    def default_volume_uom():
        '''
        product
            - preset our custom volume
        '''
        ModelData = Pool().get('ir.model.data')
        return ModelData.get_id('product', 'uom_liter')

    def get_products_displayed_on_eshop(self, name=None):
        '''
        nereid_catalog
          - Return the variants sorted by display_squence
        '''
        Product = Pool().get('product.product')
        return list(map(int, Product.search([
                    ('template', '=', self.id),
                    ('displayed_on_eshop', '=', True),
                    ], order=[('display_sequence', 'ASC')])))

    @classmethod
    def copy(cls, templates, default=None):
        '''
        product
          - We don't want the actual variants to be copied
        '''
        if default is None:
            default = {}
        default = default.copy()

        default.setdefault('products', None)
        return super(Template, cls).copy(templates, default)

    @classmethod
    def write(cls, *args):
        '''
        We toggle the active state of the variants according to the setting
        of the template
        '''
        pool = Pool()
        Product = pool.get('product.product')

        to_activate = []
        to_deactivate = []
        actions = iter(args)
        for templates, values in zip(actions, actions):
            if 'active' in values:
                with Transaction().set_context(active_test=False):
                    for template in templates:
                        template, = cls.browse([template.id])
                        if values['active']:
                            to_activate.extend([p for p in template.products])
                        else:
                            to_deactivate.extend([
                                p for p in template.products if p.active])
        super().write(*args)

        product_args = []
        if to_activate:
            product_args.extend((to_activate, {'active': True}))
        if to_deactivate:
            product_args.extend((to_deactivate, {'active': False}))
        if product_args:
            Product.write(*product_args)


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    purchasable = fields.Function(fields.Boolean('Purchasable', states={
            'readonly': ~Eval('active', True),
            },
            help='Note: This field is displayed for convenience on the '
                 'variant, but refers to the template.',
            ), 'get_template', searcher='search_template',
        setter='set_template')
    salable = fields.Function(fields.Boolean('Salable', states={
            'readonly': ~Eval('active', True),
            },
            help='Note: This field is displayed for convenience on the '
                 'variant, but refers to the template.',
            ), 'get_template', searcher='search_template',
        setter='set_template')
    display_sequence = fields.Integer('Display Sequence', states={
            'invisible': ~Eval('displayed_on_eshop', False)
            },
            help='Determines the sequence of the display in the Web Shop')
    customer_price_uom = fields.Function(fields.Numeric('Customer Price',
        digits=price_digits), 'get_customer_price_uom')

    @classmethod
    def __setup__(cls):
        super(Product, cls).__setup__()
        # disable required for prices on variant to be able to create templates
        # with a default product
        # (required ist property, nicht state!)
        cls.list_price.required = False
        cls.cost_price.required = False

    '''
    Provide short lived caches for product prices

    A cache duration of 10 min should be adequate for returning requests inside
    one session, this will also be the delay for evtl. occuring price updates
    '''
    # _sale_price_cache was moved to nereid_cart_b2c (#4218)
    # _sale_price_cache = Cache('product.product.sale_price', duration=10 * 60)
    _list_price_with_vat_cache = Cache(
        'product.product.list_price_with_vat', duration=10 * 60)

    def get_rec_name(self, name=None):
        '''
        Add the available quantity after the rec_name
          - for use in sale line views
        Note: This is the only performant way to get quantities displayed in
        the autocompletion of products on sale lines
        '''
        res = super(Product, self).get_rec_name(name)
        if (Transaction().context.get('with_quantity')
                and self.type in ['goods', 'kit']):
            res += ' (%s, %s)' % (self.quantity, self.forecast_quantity)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        '''
        Do not follow issue7437 upstream to remove the wildcard on the code
        search. We want to be able to search on parts of the product code
        without putting manually wildcards.
        '''
        if clause[1].startswith('!') or clause[1].startswith('not '):
            bool_op = 'AND'
        else:
            bool_op = 'OR'
        #code_value = clause[2]
        #if clause[1].endswith('like'):
        #    code_value = lstrip_wildcard(clause[2])
        return [bool_op,
            #('code', clause[1], code_value) + tuple(clause[3:]),
            ('code',) + tuple(clause[1:]),
            ('template.name',) + tuple(clause[1:]),
            ]

    @staticmethod
    def default_display_available_quantity():
        '''
        nereid_cart_b2c
            - set our usual preference
        '''
        return True

    @staticmethod
    def default_start_displaying_available_quantity():
        '''
        nereid_cart_b2c
            - set our usual preference
        '''
        return 0

    @staticmethod
    def get_customer_price_uom(products, name):
        '''
        Needs the necessary values for the computation in the context.
        Those are set to the context of field 'lines' in sale.py.
        '''
        pool = Pool()
        Product = pool.get('product.product')
        prices = Product.get_sale_price(products)
        return prices

    def get_default_image(self, name):
        '''
        Try to get the image from the first node if there is no image defined
        for the product.
        Caveat:
            get_default_image is originally in nereid_catalog, but
            hard overriden in nereid_webshop to provide the fallback!
            So we must super at the end.
        '''
        if not self.images:
            if self.nodes:
                res = self.nodes[0].node.default_image.id
                if res:
                    return res
        return super(Product, self).get_default_image(name)

    def compute_shipping_date(self, date=None):
        '''
        sale/product.py
         - Compute the shipping date on the base of available suppliers
           (lead_time on product_suppliers) and not only on the base of
           the lead_time on the template (#2823).

        As we are doing supply_on_sale for products without order point, we
        must take care to have a correct planned delivery date on the sale
        line.
        This is also needed in order to trigger the choice of the correct
        supplier in sale_supply/stock_supply (#2638).
          - calculate a prospective delivery date for products not on stock
            (depends sale_delivery_date)
        Cascade:
            - on_change_with_shipping_date:
                sale_delivery_date
                sale
              - product.compute_shipping_date
                sale/product.py
                -> relates to delivery_time on product.template
        '''
        pool = Pool()
        Request = pool.get('purchase.request')
        Channel = pool.get('sale.channel')

        date = super(Product, self).compute_shipping_date(date)

        current_channel = Channel(Transaction().context.get('current_channel'))
        context = {
            'locations': [current_channel.warehouse.storage_location.id],
        }
        with Transaction().set_context(**context):
            product, = self.__class__.browse([self.id])
            available_quantity = product.quantity

        if self.type in ('goods', 'assets', 'kit'):
            # When a lead time is defined, we use that (already calculated with super)
            if self.lead_time != datetime.timedelta(0):
                return date
            # If the product is not available, take the supply time of the
            # supplier as delivery date. In case we can only partly satisfy
            # the complete quantity, the missing quantity will be triggered by
            # the creation of purchase requests.
            elif available_quantity <= 0:
                if self.type == 'kit':
                    for component in self.components:
                        min_date, max_date = Request.get_supply_dates(
                            component.product)
                        date = max(date, min_date)
                else:
                    min_date, max_date = Request.get_supply_dates(self)
                    date = min_date
        return date

    def inventory_status(self):
        '''
        nereid_cart_b2c
            - Provide our own simplified implementation with custom status
              messages.
        '''
        pool = Pool()
        Move = pool.get('stock.move')
        Location = pool.get('stock.location')

        def get_draft_moves(product, locations):
            draft_moves = Move.search([
                    ('product', '=', product.id),
                    ('state', '=', 'draft'),
                    ('to_location', 'in', locations),
                    ])
            return draft_moves

        quantity = self.get_availability().get('quantity')
        if self.can_buy_from_eshop(quantity):
            status = 'in_stock'
            quantity = int(quantity)
            if quantity <= 0:
                if self.min_warehouse_quantity is None:
                    status, message = 'not_available', str(
                        _('Not available'))
                    return status, message

                in_locations = Location.search([
                        ('code', 'in', ['IN', 'STO']),
                        ('parent', '=',
                            current_website.stock_location.warehouse.id),
                        ])
                ordered = False
                if self.type == 'kit':
                    for component in self.components:
                        if get_draft_moves(component.product, in_locations):
                            ordered = True
                            break
                else:
                    if get_draft_moves(self, in_locations):
                        ordered = True

                if ordered:
                    message = str(_('Ordered, available soon'))
                else:
                    if self.type == 'kit':
                        message = str(_('Currently out of stock or only '
                                'partly available, will be ordered'))
                    else:
                        message = str(
                            _('Currently out of stock, will be ordered'))
            else:
                message = str(_('In stock'))
        else:
            status, message = 'out_of_stock', str(_('Out of stock'))
        return status, message

    def get_availability(self):
        '''
        nereid_cart_b2c
            - Override: Do not calculate the forecast quantity, it is not used
        '''
        context = {
            'locations': [current_website.stock_location.id],
        }
        with Transaction().set_context(**context):
            return {
                'quantity': self.get_quantity([self], 'quantity')[self.id],
            }

    def _get_kit_price_list(self):
        '''
        Provide an extensible method to specify distinct pricelists for the
        calculation of kit products (based on sale price of their
        components), e.g. for use with nested pricelists
        '''
        PriceList = Pool().get('product.price_list')
        pricelist = PriceList.search([
                ('name', '=', 'Standard'),
                ])
        if pricelist:
            return pricelist[0].id
        return super()._get_kit_price_list()

    def sale_price(self, quantity=0):
        """
        Extend sale_price from nereid_cart_b2c to show prices with/without tax
        according to the setting price_display on the website. (#2486)

        Return the Sales Price.
        A wrapper designed to work as a context variable in templating

        The price is calculated from the pricelist associated with the current
        user. The user in the case of guest user is logged in user. In the
        event that the logged in user does not have a pricelist set against
        the user, the guest user's pricelist is chosen.

        Finally if neither the guest user, nor the regsitered user has a
        pricelist set against them then the list price is displayed as the
        list price of the product

        :param quantity: Quantity
        """
        pool = Pool()
        Tax = pool.get('account.tax')
        Sale = pool.get('sale.sale')
        if current_website.price_display == 'no_tax':
            price = super(Product, self).sale_price(quantity=quantity)
        elif current_website.price_display == 'with_tax':
            '''
            This is a verbatim monkey patch of sale_price in nereid_cart_b2c,
            but with tax included in order to provide the same cache for the
            sale price.
            '''
            price_list = Sale.default_price_list()

            if current_user.is_anonymous:
                customer = current_website.guest_user.party
            else:
                customer = current_user.party

            # Set the current_user into the context to get unique cache entries
            # per user (#4298)
            with Transaction().set_context(current_user=current_user.id):
                price = self._sale_price_cache.get(self.id)
                if price is not None:
                    return price
                price_context = {
                    'customer': customer.id,
                    'price_list': price_list,
                    'currency': current_locale.currency.id,
                    }
                with Transaction().set_context(**price_context):
                    price = self.get_sale_price([self], quantity)[self.id]
                    taxes = Tax.compute(self.template.customer_taxes_used,
                        price, 1.0)
                    for tax in taxes:
                        price += tax['amount']
                    digits = self.__class__.list_price.digits[1]
                    price = price.quantize(Decimal(str(10 ** - digits)))
                self._sale_price_cache.set(self.id, price)
        else:
            # do not proceed without price display configuration
            raise('no price display configuration for website found')
        return price

    def list_price_with_vat(self, quantity=0):
        '''
        This is a verbatim monkey patch of sale_price in nereid_cart_b2c,
        but with tax included in order to provide the same cache for the
        list price. (#2486)
        '''
        pool = Pool()
        Tax = pool.get('account.tax')
        Sale = pool.get('sale.sale')
        price_list = Sale.default_price_list()

        if current_user.is_anonymous:
            customer = current_website.guest_user.party
        else:
            customer = current_user.party

        price = self._list_price_with_vat_cache.get(self.id)
        if price is not None:
            return price
        with Transaction().set_context(customer=customer.id,
                price_list=price_list,
                currency=current_locale.currency.id):
            price = self.list_price
            taxes = Tax.compute(self.template.customer_taxes_used,
                price, 1.0)
            for tax in taxes:
                price += tax['amount']
            digits = self.__class__.list_price.digits[1]
            price = price.quantize(Decimal(str(10 ** - digits)))
        self._list_price_with_vat_cache.set(self.id, price)
        return price

    def get_absolute_url(self, **kwargs):
        '''
        nereid_catalog
          - Don't fail on missing URIs (e.g. shipping costs)
        '''
        if not self.uri:
            return None
        return super(Product, self).get_absolute_url(**kwargs)

    def serialize(self, purpose=None):
        '''
        nereid_catalog_variants
        - Adding additional values needed in the templating
        '''
        res = super(Product, self).serialize(purpose)
        if purpose != 'variant_selection':
            return res

        currency_format = partial(
            numbers.format_currency,
            currency=current_website.company.currency.code,
            locale=current_website.default_locale.language.code
        )

        if current_website.price_display == 'with_tax':
            list_price_wo_format = self.list_price_with_vat(1)
        else:
            list_price_wo_format = self.list_price
        # Decimal can not be dumped to json, we must convert to float
        res['price_wo_format'] = float(self.sale_price(1))
        res['list_price'] = currency_format(list_price_wo_format)
        res['list_price_wo_format'] = float(list_price_wo_format)
        return res

    @classmethod
    def create(cls, vlist):
        products = super(Product, cls).create(vlist)
        cls.update_channel_listing(products)
        return products

    @classmethod
    def write(cls, *args):
        super().write(*args)
        actions = iter(args)
        for products, values in zip(actions, actions):
            cls.update_channel_listing(products)
            if any(True for k in values.keys()
                    if k in ['active', 'displayed_on_eshop']):
                cls.update_tree_nodes(products)

    @classmethod
    def update_channel_listing(cls, products):
        pool = Pool()
        Channel = pool.get('sale.channel')
        ChannelListing = pool.get('product.product.channel_listing')

        webshop_channels = Channel.search([
                ('source', '=', 'webshop'),
                ])
        # We use the uri as the general product_identifier for all channels
        for product in products:
            if not product.active:
                listings = ChannelListing.search([
                        ('product', '=', product.id),
                        ])
                ChannelListing.delete(listings)
            else:
                if product.displayed_on_eshop:
                    for channel in webshop_channels:
                        listings = ChannelListing.search([
                                ('product', '=', product.id),
                                ('channel', '=', channel.id),
                                ])
                        if listings:
                            listing = listings[0]
                            if listing.product_identifier != product.uri:
                                listing.product_identifier = product.uri
                            listing.state = 'active'
                            listing.save()
                        else:
                            listing = ChannelListing()
                            listing.channel = channel.id
                            listing.product = product.id
                            listing.product_identifier = product.uri
                            listing.state = 'active'
                            listing.save()
                else:
                    for channel in webshop_channels:
                        listings = ChannelListing.search([
                                ('product', '=', product.id),
                                ('channel', '=', channel.id),
                                ])
                        if listings:
                            listing = listings[0]
                            listing.state = 'disabled'
                            listing.save()

    @classmethod
    def update_tree_nodes(cls, products):
        pool = Pool()
        Node = pool.get('product.tree_node')

        def get_parent(node, active):
            parent = node.parent
            rv = []
            if (parent
                    and (active and parent.active != active)
                    or (not active and len(parent.children) <= 1)):
                rv.append(parent)
                rv.extend(get_parent(parent, active))
            return rv

        def get_children(node):
            rv = []
            for child in node.children:
                rv.append(child)
                rv.extend(get_children(child))
            return rv

        nodes = [(node.node, product.active, product.displayed_on_eshop)
            for product in products
            for node in product.nodes]
        for node, p_active, displayed_on_eshop in nodes:
            active = displayed_on_eshop and p_active
            if active:
                to_activate = []
                with Transaction().set_context(active_test=False):
                    node, = Node.browse([node.id])
                    to_activate.append(node)
                    to_activate.extend(get_parent(node, active))
                    to_activate.extend(get_children(node))
                if to_activate:
                    Node.write(to_activate, {'active': True})

            else:
                to_deactivate = []
                to_deactivate.append(node)
                to_deactivate.extend(get_parent(node, active))
                to_deactivate.extend(get_children(node))
                if to_deactivate:
                    Node.write(to_deactivate, {'active': False})

    @classmethod
    def copy(cls, products, default=None):
        '''
        product
          - We want unique product codes
        '''
        if default is None:
            default = {}
        default = default.copy()

        duplicate_products = []
        for index, product in enumerate(products, start=1):
            if product.code:
                default['code'] = "%s-copy-%d" % (product.code, index)
            duplicate_products.extend(
                super(Product, cls).copy([product], default)
            )
        return duplicate_products

    def get_meta_description(self):
        '''
        Provide a useful description for the meta description tag
        https://support.google.com/webmasters/answer/79812?hl=en&ref_topic=4617741
        https://support.google.com/webmasters/answer/35624?rd=1#1
            <meta name="Description" CONTENT="Author: A.N. Author,
            Illustrator: P. Picture, Category: Books, Price:  £9.24,
            Length: 784 pages">
        '''
        description = '%s, Kategorie: %s' % (self.name,
            self.account_category.name)
        if self.brand:
            description += ', Hersteller: %s' % (self.brand.rec_name,)
        return Markup(description)

    @classmethod
    @route('/sitemaps/product-index.xml', defaults={'priority': 0.5})
    @route('/sitemaps/product-index.xml/<priority>')
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
    @route('/sitemaps/product-<int:page>.xml?priority=<priority>')
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
        product groups.
        prio 0.5 = default all with prio 0.5

        Strategy:
            - basically we use the defined top level categories to get their
              children
                - take care to use those categories only once
        '''
        pool = Pool()
        Category = pool.get('product.category')

        domain = [
                ('active', '=', True),
                ('displayed_on_eshop', '=', True),
                ]
        categories = None
        if priority == '1.0':
            categories = ('Aquila', 'Toro')
        elif priority == '0.8':
            categories = ('Kolophonien', 'Pirastro', 'Gutscheine', 'Savarez')
        elif priority == '0.3':
            categories = ('Gewa', 'Winter')
        elif priority == '0.2':
            categories = ('HMI', 'Dlugolecki', 'Kürschner',
                'MSA Musik Schnerr', 'Gamut')

        if categories:
            category_ids = []
            for category_name in categories:
                categories = Category.search([
                        ('parent', 'child_of', category_name),
                        ])
                category_ids.extend([c.id for c in categories])
            or_domain = ['OR', ]
            for category_id in category_ids:
                or_domain.append(('account_category', '=', category_id))
            domain.append(or_domain)
        return domain

    def elastic_search_json(self):
        '''
        nereid_webshop_elastic_search
          - Add the brand

        '''
        res = super(Product, self).elastic_search_json()
        if self.brand:
            res['brand'] = self.brand.name
        return res

    def elastic_attributes_json(self):
        '''
        nereid_webshop_elastic_search
          - Add the brand as a pseudo attribute
        '''
        res = super(Product, self).elastic_attributes_json()
        if self.brand:
            res['Marke'] = self.brand.name
        return res

    @classmethod
    def _update_es_facets(cls, search_obj, filterable_attributes=None,
            facet_filter=None):
        '''
        nereid_webshop_elastic_search
          - Add the brand to facets
        Note: This is more or less a default filter, that will be overriden
        by the settings of an attribute with the same name!!
        '''
        search_obj.facet.add_term_facet(
            'Marke',
            facet_filter=facet_filter,
            all_terms=True,
            size=30,
            order='count'
        )
        super(Product, cls)._update_es_facets(search_obj,
            filterable_attributes=filterable_attributes,
            facet_filter=facet_filter)



    @classmethod
    def _build_es_query(cls, search_phrase):
        """
        Return an instance of `~pyes.query.Query` for the given phrase.
        If downstream modules wish to alter the behavior of search, for example
        by adding more fields to the query or changing the ranking in a
        different way, this would be the method to change.
        """
        return BoolQuery(
            should=[
                MatchQuery(
                    'code', search_phrase, boost=1.5
                ),
                MatchQuery(
                    'name', search_phrase, boost=2
                ),
                MatchQuery(
                    'name.partial', search_phrase
                ),
                MatchQuery(
                    'name.metaphone', search_phrase
                ),
                MatchQuery(
                    'description', search_phrase, boost=0.5
                ),
                MatchQuery(
                    'brand', search_phrase, boost=1.5
                ),
                MatchQuery(
                    'category.name', search_phrase
                ),
                NestedQuery(
                    'tree_nodes', BoolQuery(
                        should=[
                            MatchQuery(
                                'tree_nodes.name',
                                search_phrase
                            ),
                        ]
                    )
                ),
            ],
            must=[
                MatchQuery(
                    'active', "true"
                ),
                MatchQuery(
                    'displayed_on_eshop', "true"
                ),
            ]
        )

    @classmethod
    def _build_es_filter(cls, filterable_attributes=None):
        '''
        nereid_webshop_elastic_search
          - Use the pseudo attribute brand to construct a filter
        '''
        main_filter = super(Product, cls)._build_es_filter(
            filterable_attributes=filterable_attributes)

        # Search for the attribute name 'Marke' in request.args.
        # If present (meaning it is a valid argument), add it as a TermFilter.
        and_filter_list = []
        for key in request.args:
            if key == 'Marke':
                or_filter = ORFilter(
                    [
                        TermFilter(key, value) for value
                        in request.args.getlist(key)
                    ]
                )
                and_filter_list.append(or_filter)

        # Add the filter(s) (if present) to the main_filter
        if and_filter_list:
            and_filter = ANDFilter(and_filter_list)
            if not main_filter:
                main_filter = BoolFilter()
            main_filter.add_must(and_filter)
        return main_filter


class ProductSupplier(metaclass=PoolMeta):
    __name__ = 'purchase.product_supplier'

    def compute_supply_date(self, date=None):
        '''
        purchase/product.py
        Contrary to upstream we want an empty lead time field not to mean
        datetime.date.max, but immediate supply. So we convert simply
        datetime.date.max to today.
        '''
        Date = Pool().get('ir.date')

        supply_date = super(ProductSupplier, self).compute_supply_date(
            date=date)
        if supply_date == datetime.date.max:
            return Date.today()
        return supply_date


def add_domain_other(_cls):
    '''
    account_product/product.py
    Remove the revenue/expense domain on accounts in accounting
    categories
    This is needed to create accounting categories writing to statement
    accounts like 'Durchlaufende Posten', for e.g. contracts.
    With 5.2 we lost the possibility to define accounts on the product,
    thus we need that on level of the accounting categories.
    '''
    other = ('type.other', '=', True)
    revenue = ('type.revenue', '=', True)
    expense = ('type.expense', '=', True)
    revenue_domain = _cls.account_revenue.domain
    if other not in revenue_domain:
        revenue_domain.remove(revenue)
        revenue_domain += [
            ['OR',
            revenue,
            other],]
    expense_domain = _cls.account_expense.domain
    if other not in expense_domain:
        expense_domain.remove(expense)
        expense_domain += [
            ['OR',
            expense,
            other],]


class Category(metaclass=PoolMeta):
    __name__ = 'product.category'

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()
        add_domain_other(cls)


class CategoryAccount(metaclass=PoolMeta):
    __name__ = 'product.category.account'

    @classmethod
    def __setup__(cls):
        super(CategoryAccount, cls).__setup__()
        add_domain_other(cls)

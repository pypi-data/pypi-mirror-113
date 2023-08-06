# This file is part esale_product module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard, StateTransition, StateView, Button
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.modules.product_esale.tools import slugify
from simpleeval import simple_eval
from trytond.exceptions import UserError
from trytond.i18n import gettext

__all__ = ['Template', 'Product', 'EsaleAttributeGroup', 'EsaleExportStart',
    'EsaleExportResult', 'EsaleExportProduct', 'EsaleExportPrice',
    'EsaleExportImage', 'EsaleExportCSVStart', 'EsaleExportCSVResult',
    'EsaleExportCSV']


class EsaleAttributeGroup(ModelSQL, ModelView):
    'Esale Attribute Group'
    __name__ = 'esale.attribute.group'
    name = fields.Char('Name', required=True)
    code = fields.Char('Code', required=True)
    active = fields.Boolean('Active')

    @staticmethod
    def default_active():
        return True


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    esale_attribute_group = fields.Many2One('esale.attribute.group',
        'eSale Attribute',
        help="Attribute in e-commerce plattaform")

    @staticmethod
    def default_esale_attribute_group():
        Config = Pool().get('product.configuration')
        config = Config(1)
        return config.esale_attribute_group.id \
            if config.esale_attribute_group else None


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'

    @classmethod
    def esale_export_domain(cls, shop, from_date):
        'eSale Export Domain'
        # get domain from esale APP or new domain
        if shop.esale_shop_app:
            product_domain = getattr(cls, '%s_product_domain' % shop.esale_shop_app)
            domain = product_domain([shop.id])
        else:
            domain = [
                ('esale_available', '=', True),
                ('code', '!=', None),
                ]
        if from_date:
            domain += [['OR',
                        ('create_date', '>=', from_date),
                        ('write_date', '>=', from_date),
                        ('template.create_date', '>=', from_date),
                        ('template.write_date', '>=', from_date),
                    ]]
        return domain

    @classmethod
    def esale_export_csv(cls, shop, lang, from_date=None):
        'eSale Export CSV'
        domain = cls.esale_export_domain(shop, from_date)
        products = cls.search(domain)

        export_csv = getattr(cls, 'esale_export_csv_%s' % shop.esale_shop_app)
        output = export_csv(shop, products, lang)
        return output


class EsaleExportStart(ModelView):
    'Export Tryton to External Shop: Start'
    __name__ = 'esale.export.start'
    shops = fields.One2Many('sale.shop', None, 'Shops')
    shop = fields.Many2One('sale.shop', 'Shop', required=True,
        domain=[
            ('id', 'in', Eval('shops')),
        ], depends=['shops'],
        help='Select shop will be export this product.')


class EsaleExportResult(ModelView):
    'Export Tryton to External Shop: Result'
    __name__ = 'esale.export.result'
    info = fields.Text('Info', readonly=True)


class EsaleExportProduct(Wizard):
    'Export Products Tryton to External Shop'
    __name__ = "esale.export.product"

    start = StateView('esale.export.start',
        'esale_product.esale_export_start', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Export', 'export', 'tryton-ok', default=True),
            ])
    export = StateTransition()
    result = StateView('esale.export.result',
        'esale_product.esale_export_result', [
            Button('Close', 'end', 'tryton-close'),
            ])

    @classmethod
    def __setup__(cls):
        super(EsaleExportProduct, cls).__setup__()

    def default_start(self, fields):
        Template = Pool().get('product.template')
        templates = Template.browse(Transaction().context['active_ids'])
        shops = [s.id for t in templates for s in t.shops
            if s.esale_available]
        if not shops:
            return {}
        return {
            'shops': shops,
            'shop': shops[0],
            }

    def transition_export(self):
        Template = Pool().get('product.template')
        shop = self.start.shop
        export_status = getattr(shop,
            'export_products_%s' % shop.esale_shop_app)
        templates = Template.browse(Transaction().context['active_ids'])
        templates = [t.id for t in templates if shop in t.shops]
        export_status(templates)
        try:
            raise UserError(gettext('export_info',
                    prices=','.join(str(t) for t in templates),
                    shop=shop.rec_name))
        except UserError as e:
            self.result.info = e

        return 'result'

    def default_result(self, fields):
        info_ = self.result.info
        return {
            'info': info_,
            }


class EsaleExportPrice(Wizard):
    """Export Prices Tryton to External Shop"""
    __name__ = "esale.export.price"

    start = StateView('esale.export.start',
        'esale_product.esale_export_start', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Export', 'export', 'tryton-ok', default=True),
            ])
    export = StateTransition()
    result = StateView('esale.export.result',
        'esale_product.esale_export_result', [
            Button('Close', 'end', 'tryton-close'),
            ])

    def default_start(self, fields):
        Template = Pool().get('product.template')
        templates = Template.browse(Transaction().context['active_ids'])
        shops = [s.id for t in templates for s in t.shops
            if s.esale_available]
        if not shops:
            return {}
        return {
            'shops': shops,
            'shop': shops[0],
            }

    def transition_export(self):
        shop = self.start.shop
        export_status = getattr(shop, 'export_prices_%s' % shop.esale_shop_app)
        templates = Transaction().context['active_ids']
        export_status(templates)
        try:
            raise UserError(gettext('export_info',
                    prices=','.join(str(t) for t in templates),
                    shop=shop.rec_name))
        except UserError as e:
            self.result.info = e

        return 'result'

    def default_result(self, fields):
        info_ = self.result.info
        return {
            'info': info_,
            }


class EsaleExportImage(Wizard):
    """Export Images Tryton to External Shop"""
    __name__ = "esale.export.image"

    start = StateView('esale.export.start',
        'esale_product.esale_export_start', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Export', 'export', 'tryton-ok', default=True),
            ])
    export = StateTransition()
    result = StateView('esale.export.result',
        'esale_product.esale_export_result', [
            Button('Close', 'end', 'tryton-close'),
            ])

    def default_start(self, fields):
        Template = Pool().get('product.template')
        templates = Template.browse(Transaction().context['active_ids'])
        shops = [s.id for t in templates for s in t.shops if s.esale_available]
        if not shops:
            return {}
        return {
            'shops': shops,
            'shop': shops[0],
            }

    def transition_export(self):
        shop = self.start.shop
        export_status = getattr(shop, 'export_images_%s' % shop.esale_shop_app)
        templates = Transaction().context['active_ids']
        export_status(templates)
        try:
            raise UserError(gettext('export_info',
                    prices=','.join(str(t) for t in templates),
                    shop=shop.rec_name))
        except UserError as e:
            self.result.info = e

        return 'result'

    def default_result(self, fields):
        info_ = self.result.info
        return {
            'info': info_,
            }


class EsaleExportCSVStart(ModelView):
    'eSale Export CSV Start'
    __name__ = 'esale.export.csv.start'
    shop = fields.Many2One('sale.shop', 'Shop', required=True,
        domain=[('esale_available', '=', True)])
    language = fields.Many2One('ir.lang', 'Language', required=True,
        domain=[('translatable', '=', True)])
    from_date = fields.DateTime('From Date',
        help='Filter products create/write from this date. '
        'An empty value are all catalog product.')

    @staticmethod
    def default_shop():
        User = Pool().get('res.user')
        user = User(Transaction().user)
        return user.shop.id if (user.shop and user.shop.esale_available) else None

    @staticmethod
    def default_language():
        User = Pool().get('res.user')
        user = User(Transaction().user)
        return user.language.id if user.language else None


class EsaleExportCSVResult(ModelView):
    'eSale Export CSV Result'
    __name__ = 'esale.export.csv.result'
    csv_file = fields.Binary('CSV', filename='file_name')
    file_name = fields.Text('File Name')


class EsaleExportCSV(Wizard):
    'eSale Export CSV'
    __name__ = "esale.export.csv"
    start = StateView('esale.export.csv.start',
        'esale_product.esale_export_csv_start', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Export', 'export', 'tryton-ok', default=True),
            ])
    export = StateTransition()
    result = StateView('esale.export.csv.result',
        'esale_product.esale_export_csv_result', [
            Button('Close', 'end', 'tryton-close'),
            ])

    def transition_export(self):
        Product = Pool().get('product.product')

        shop = self.start.shop
        lang = self.start.language.code
        from_date = self.start.from_date

        output = Product.esale_export_csv(shop, lang, from_date)

        self.result.csv_file = fields.Binary.cast(output.getvalue())
        if shop.esale_export_product_filename:
            context = shop.get_export_csv_context_formula(lang)
            filename = simple_eval(shop.esale_export_product_filename, **context)
        else:
            filename = '%s-%s.csv' % (
                slugify(shop.name.replace('.', '-')),
                lang.split('_')[0], # TODO 4.2 no split locale code
                )
        self.result.file_name = filename
        return 'result'

    def default_result(self, fields):
        return {
            'csv_file': self.result.csv_file,
            'file_name': self.result.file_name,
            }

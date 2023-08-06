# This file is part esale_product module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.pool import PoolMeta
from trytond.exceptions import UserError
from trytond.i18n import gettext

__all__ = ['SaleShop']


class SaleShop(metaclass=PoolMeta):
    __name__ = 'sale.shop'
    esale_last_products = fields.DateTime('Last Products',
        help='This date is last export (filter)')
    esale_last_prices = fields.DateTime('Last Prices',
        help='This date is last export (filter)')
    esale_last_images = fields.DateTime('Last Images',
        help='This date is last export (filter)')
    esale_last_menus = fields.DateTime('Last Menus',
        help='This date is last export (filter)')
    esale_top_menu = fields.Many2One('esale.catalog.menu', 'Top Menu')
    esale_export_product_filename = fields.Char('eSale Export Product Filename',
        help='Python expression that will be evaluated to generate the filename.\n'
            'If is empty, export the filename as <shopname>-<lang>.csv.')

    @classmethod
    def __setup__(cls):
        super(SaleShop, cls).__setup__()
        cls._buttons.update({
                'export_products': {},
                'export_prices': {},
                'export_images': {},
                'export_menus': {},
                })

    @classmethod
    @ModelView.button
    def export_products(cls, shops):
        """
        Export Products to External APP
        """
        for shop in shops:
            if not shop.esale_last_products:
                raise UserError(gettext('select_date_products'))
            export_products = getattr(shop,
                'export_products_%s' % shop.esale_shop_app)
            export_products()

    @classmethod
    @ModelView.button
    def export_prices(self, shops):
        """
        Export Prices to External APP
        """
        for shop in shops:
            if not shop.esale_last_prices:
                raise UserError(gettext('select_date_prices'))
            export_prices = getattr(shop,
                'export_prices_%s' % shop.esale_shop_app)
            export_prices()

    @classmethod
    @ModelView.button
    def export_images(self, shops):
        """
        Export Images to External APP
        """
        for shop in shops:
            if not shop.esale_last_images:
                raise UserError(gettext('select_date_images'))
            export_images = getattr(shop,
                'export_images_%s' % shop.esale_shop_app)
            export_images()

    @classmethod
    @ModelView.button
    def export_menus(self, shops):
        """
        Export Menus to External APP
        """
        for shop in shops:
            if not shop.esale_top_menu:
                raise UserError(gettext('menu_not_export'))
            if not shop.esale_last_menus:
                raise UserError(gettext('select_date_menus'))
            export_menus = getattr(shop,
                'export_menus_%s' % shop.esale_shop_app)
            export_menus()

    def export_products_tryton(self, shop):
        """Export Products to Tryton e-Sale
        :param shop: Obj
        """
        # TODO: Export Tryton product
        # active_ids = Transaction().context.get('active_ids')
        return True

    def export_prices_tryton(self, shop):
        """Export Prices to Tryton e-Sale
        :param shop: Obj
        """
        # TODO: Export Tryton prices
        # active_ids = Transaction().context.get('active_ids')
        return True

    def export_images_tryton(self, shop):
        """Export Images to Tryton e-Sale
        :param shop: Obj
        """
        # TODO: Export Tryton images
        # active_ids = Transaction().context.get('active_ids')
        return True

    def export_menus_tryton(self, shop):
        """Export Menus to Tryton e-Sale
        :param shop: Obj
        """
        # TODO: Export Tryton menus
        return True

    @classmethod
    def export_cron_product(cls):
        """
        Cron export product
        """
        shops = cls.search([
            ('esale_available', '=', True),
            ('esale_scheduler', '=', True),
            ])
        cls.export_products(shops)
        return True

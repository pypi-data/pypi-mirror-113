#!/usr/bin/env python3
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.

import io
import os
import re
from configparser import ConfigParser
from setuptools import setup, find_packages

MODULE2PREFIX = {
    # 'account': 'm9s',
    'account_banking_import': 'm9s',
    'account_banking_import_hibiscus': 'm9s',
    'account_batch': 'm9s',
    # 'account_credit_limit': 'm9s',
    'account_de': 'm9s',
    'account_deposit': 'm9s',
    'account_de_euer': 'm9s',
    'account_de_euer_zone': 'm9s',
    'account_de_skr03': 'm9s',
    # 'account_dunning': 'm9s',
    # 'account_dunning_letter': 'm9s',
     'account_invoice': 'm9s',
    'account_invoice_discount': 'm9s',
    # 'account_invoice_party_currency': 'm9s',
    # 'account_invoice_price_list': 'm9s',
    'account_invoice_purchase_supplier': 'm9s',
    'account_invoice_report_filestore': 'm9s',
    # 'account_invoice_stock': 'm9s',
    # 'account_product': 'm9s',
    # 'account_statement': 'm9s',
    'account_tax_recapitulative_statement': 'm9s',
    'account_tax_reverse_charge': 'm9s',
    'account_tax_rule_zone': 'm9s',
    'account_tax_rule_zone_eu': 'm9s',
    # 'bank': 'm9s',
    # 'babi': 'm9s',
    # 'babi_reports_product': 'm9s',
    # 'babi_reports_sale': 'm9s',
    # 'babi_reports_stock': 'm9s',
    # 'carrier': 'm9s',
    # 'carrier_weight': 'm9s',
    'carrier_weight_volume_combined': 'm9s',
    # 'company': 'm9s',
    'contract': 'm9s',
    # 'country': 'm9s',
    'country_zip': 'm9s',
    # 'currency': 'm9s',
    'customs': 'm9s',
    'customs_value': 'm9s',
    'elastic_search': 'm9s',
    'electronic_mail': 'm9s',
    'gift_card': 'm9s',
    # 'html_report': 'm9s',
    'invoice_payment_gateway': 'm9s',
    'nereid': 'm9s',
    'nereid_cart_b2c': 'm9s',
    'nereid_catalog': 'm9s',
    'nereid_catalog_tree': 'm9s',
    'nereid_catalog_variants': 'm9s',
    'nereid_checkout': 'm9s',
    'nereid_cms': 'm9s',
    'nereid_image_transformation': 'm9s',
    'nereid_payment_gateway': 'm9s',
    'nereid_shipping': 'm9s',
    'nereid_webshop': 'm9s',
    'nereid_webshop_elastic_search': 'm9s',
    'nereid_wishlist': 'm9s',
    'newsletter': 'm9s',
    # 'party': 'm9s',
    'party_address_type_strict': 'm9s',
    'party_type': 'm9s',
    'party_vcarddav': 'm9s',
    'payment_gateway': 'm9s',
    'payment_gateway_paypal': 'm9s',
    'payment_gateway_stripe': 'm9s',
    'printer_cups': 'm9s',
    # 'product': 'm9s',
    'product_attribute_strict': 'm9s',
    # 'product_brand': 'm9s',
    'product_kit': 'm9s',
    # 'product_measurements': 'm9s',
    # 'product_price_list': 'm9s',
    # 'product_price_list_formula': 'm9s',
    # 'product_price_list_price_category': 'm9s',
    'product_variant': 'm9s',
    'purchase': 'm9s',
    'purchase_discount': 'm9s',
    'purchase_request': 'm9s',
    # 'purchase_supplier_discount': 'm9s',
    'purchase_supplier_lead_time': 'm9s',
    # 'res': 'm9s',
    'sale': 'm9s',
    'sale_available_stock': 'm9s',
    'sale_channel': 'm9s',
    'sale_channel_payment_gateway': 'm9s',
    # 'sale_credit_limit': 'm9s',
    'sale_discount': 'm9s',
    # 'sale_delivery_date': 'm9s',
    # 'sale_invoice_grouping': 'm9s',
    'sale_kit': 'm9s',
    'sale_payment_channel': 'm9s',
    'sale_payment_gateway': 'm9s',
    'sale_pos_channel': 'm9s',
    # 'sale_price_list': 'm9s',
    # 'sale_price_list_recompute_price': 'm9s',
    'sale_price_with_tax': 'm9s',
    # 'sale_recompute_price': 'm9s',
    # 'sale_shipment_cost': 'm9s',
    # 'sale_shipment_grouping': 'm9s',
    # 'sale_supply': 'm9s',
    'sale_supply_state': 'm9s',
    'shipping': 'm9s',
    'smtp': 'm9s',
    # 'stock': 'm9s',
    'stock_inventory_expected_quantity': 'm9s',
    'stock_kit': 'm9s',
    # 'stock_package': 'm9s',
    # 'stock_package_shipping': 'm9s',
    'stock_package_shipping_label_filestore': 'm9s',
    'stock_package_shipping_gls': 'm9s',
    'stock_package_shipping_sale_wizard': 'm9s',
    # 'stock_shipment_measurements': 'm9s',
    # 'stock_supply': 'm9s',
    'stock_update_planned_date': 'm9s',
    'webdav': 'm9s',
    }


def read(fname, slice=None):
    content = io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()
    if slice:
        content = '\n'.join(content.splitlines()[slice])
    return content


def get_require_version(name):
    if minor_version % 2:
        require = '%s >= %s.%s.dev0, < %s.%s'
    else:
        require = '%s >= %s.%s, < %s.%s'
    require %= (name, major_version, minor_version,
        major_version, minor_version + 1)
    return require


config = ConfigParser()
config.read_file(open(os.path.join(os.path.dirname(__file__), 'tryton.cfg')))
info = dict(config.items('tryton'))
for key in ('depends', 'extras_depend', 'xml'):
    if key in info:
        info[key] = info[key].strip().splitlines()
version = info.get('version', '0.0.1')
major_version, minor_version, _ = version.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)
name = 'm9s_meta_hmi'
download_url = 'https://gitlab.com/m9s/meta_hmi.git'
local_version = []
for build in ['CI_BUILD_NUMBER', 'CI_JOB_NUMBER', 'CI_JOB_ID']:
    if os.environ.get(build):
        local_version.append(os.environ[build])
if local_version:
    version += '+' + '.'.join(local_version)
requires = []
for dep in info.get('depends', []):
    if not re.match(r'(ir|res)(\W|$)', dep):
        prefix = MODULE2PREFIX.get(dep, 'trytond')
        requires.append(get_require_version('%s_%s' % (prefix, dep)))
requires.append(get_require_version('m9s-trytond'))

tests_require = []
dependency_links = []
if minor_version % 2:
    dependency_links.append('https://trydevpi.tryton.org/?mirror=bitbucket')

setup(name=name,
    version=version,
    description='Tryton Meta Hmi Module',
    long_description=read('README.md'),
    author='MBSolutions',
    author_email='info@m9s.biz',
    url='http://www.m9s.biz/',
    download_url=download_url,
    project_urls={
        "Bug Tracker": 'https://support.m9s.biz/',
        "Source Code": 'https://gitlab.com/m9s/meta_hmi.git',
        },
    keywords='',
    package_dir={'trytond.modules.meta_hmi': '.'},
    packages=(
        ['trytond.modules.meta_hmi'] +
        ['trytond.modules.meta_hmi.%s' % p for p in find_packages()]
        ),
    package_data={
        'trytond.modules.meta_hmi': (info.get('xml', [])
            + ['tryton.cfg', 'view/*.xml', 'locale/*.po', '*.fodt',
                'icons/*.svg', 'tests/*.rst']),
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: Bulgarian',
        'Natural Language :: Catalan',
        'Natural Language :: Chinese (Simplified)',
        'Natural Language :: Czech',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Hungarian',
        'Natural Language :: Italian',
        'Natural Language :: Persian',
        'Natural Language :: Polish',
        'Natural Language :: Portuguese (Brazilian)',
        'Natural Language :: Russian',
        'Natural Language :: Slovenian',
        'Natural Language :: Spanish',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Office/Business',
        ],
    license='GPL-3',
    python_requires='>=3.5',
    install_requires=requires,
    dependency_links=dependency_links,
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    meta_hmi = trytond.modules.meta_hmi
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    tests_require=tests_require,
    )

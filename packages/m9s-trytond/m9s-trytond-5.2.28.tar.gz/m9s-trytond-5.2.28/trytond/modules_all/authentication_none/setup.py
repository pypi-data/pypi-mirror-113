#!/usr/bin/env python3
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

import io
import os
from setuptools import setup, find_packages


def read(fname):
    return io.open(
        os.path.join(os.path.dirname(__file__), fname),
        'r', encoding='utf-8').read()


setup(name='tpf_authentication_none',
    version='0.0.1',
    description='Tryton module to authenticate using username only',
    long_description=read('README.rst'),
    author='Tryton Foundation',
    author_email='foundation@tryton.org',
    url='http://foundation.tryton.org/',
    keywords='tryton authentication none',
    package_dir={'trytond.modules.authentication_none': '.'},
    packages=(
        ['trytond.modules.authentication_none']
        + ['trytond.modules.authentication_none.%s' % p
            for p in find_packages()]
        ),
    package_data={
        'trytond.modules.authentication_none': ['tryton.cfg'],
        },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Plugins',
        'Framework :: Tryton',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Natural Language :: Bulgarian',
        'Natural Language :: Catalan',
        'Natural Language :: Czech',
        'Natural Language :: Dutch',
        'Natural Language :: English',
        'Natural Language :: Finnish',
        'Natural Language :: French',
        'Natural Language :: German',
        'Natural Language :: Hungarian',
        'Natural Language :: Indonesian',
        'Natural Language :: Italian',
        'Natural Language :: Persian',
        'Natural Language :: Polish',
        'Natural Language :: Portuguese (Brazilian)',
        'Natural Language :: Russian',
        'Natural Language :: Slovenian',
        'Natural Language :: Spanish',
        'Natural Language :: Turkish',
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
    install_requires=['trytond>=5.0'],
    zip_safe=False,
    entry_points="""
    [trytond.modules]
    authentication_none = trytond.modules.authentication_none
    """,
    test_suite='tests',
    test_loader='trytond.test_loader:Loader',
    )

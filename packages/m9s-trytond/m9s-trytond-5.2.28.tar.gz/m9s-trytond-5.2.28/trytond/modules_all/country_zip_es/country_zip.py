# This file is part of country_zip_es module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from csv import reader
from trytond.model import ModelView
from trytond.pool import Pool
from trytond.wizard import Button, StateView, Wizard, StateTransition
from trytond.tools import grouped_slice
import os
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['LoadCountryZipsStart', 'LoadCountryZips']


class LoadCountryZipsStart(ModelView):
    'Load Country Zips Start'
    __name__ = 'load.country.zips.start'


class LoadCountryZips(Wizard):
    'Load Country Zips'
    __name__ = "load.country.zips"

    start = StateView('load.country.zips.start',
        'country_zip_es.load_country_zips_start_view_form', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('Accept', 'accept', 'tryton-ok', default=True),
            ])
    accept = StateTransition()


    def transition_accept(self):
        pool = Pool()
        Subdivision = pool.get('country.subdivision')
        CountryZip = pool.get('country.zip')

        delimiter = ','
        quotechar = '"'
        with open(os.path.join(os.path.dirname(__file__), 'country_zip_es.csv'),
                'r', encoding='utf-8') as data:
            try:
                rows = list(reader(data, delimiter=delimiter,
                    quotechar=quotechar))
            except TypeError as e:
                raise UserError(gettext(
                    'country_zip_es.error', filename='country_zip_es', error=e))
            rows = rows[1:]

        records = []
        for row in rows:
            if not row:
                continue

            zips = CountryZip.search([
                    ('zip', '=', row[0]),
                    ('subdivision', '=', row[2])
                    ])
            if zips:
                zip_ = zips[0]
            else:
                zip_ = CountryZip()
                zip_.zip = row[0]
                subdivision, = Subdivision.search([
                        ('code', '=', row[2]),
                        ], limit=1)
                zip_.country = subdivision.country
                zip_.subdivision = subdivision

            zip_.city = row[1]
            records.append(zip_)
        for sub_records in grouped_slice(records):
            CountryZip.save(list(sub_records))
        return 'end'

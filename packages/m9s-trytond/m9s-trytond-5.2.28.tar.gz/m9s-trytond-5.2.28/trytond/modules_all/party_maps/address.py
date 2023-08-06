# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import urllib.request, urllib.parse, urllib.error
import sys
from geopy import geocoders
from trytond.model import ModelView, fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval, Bool
from trytond.transaction import Transaction
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Address']


class Address(metaclass=PoolMeta):
    __name__ = 'party.address'
    latitude = fields.Float('Latitude', digits=(16, 16))
    longitude = fields.Float('Longitude', digits=(16, 16))
    map_place = fields.Char('Map Place')
    map_url = fields.Function(fields.Char('Map URL'),
        'on_change_with_map_url')

    @classmethod
    def __setup__(cls):
        super(Address, cls).__setup__()
        cls._buttons.update({
                'geocode': {
                    'readonly': ~Bool(Eval('active')),
                    },
                })

    @fields.depends('name', 'street', 'streetbis', 'zip', 'city', 'country',
        'subdivision', 'latitude', 'longitude', 'map_place')
    def on_change_with_map_url(self, name=None):
        Configuration = Pool().get('party.configuration')
        config = Configuration(1)

        if not config.map_engine:
            return ''

        if self.latitude and self.longitude:
            url = '%(latitude).8f,%(longitude).8f' % {
                'latitude': self.latitude,
                'longitude': self.longitude,
                }
        elif self.map_place:
            url = self.map_place
        else:
            url = ' '.join(self.get_full_address('full_address').splitlines())
        if url.strip():
            if isinstance(url, str) and sys.version_info < (3,):
                url = url.encode('utf-8')
            geocoder_engine = getattr(self, 'map_url_%s' % config.map_engine)
            return geocoder_engine(urllib.parse.quote(url))

    @classmethod
    @ModelView.button
    def geocode(cls, addresses):
        Configuration = Pool().get('party.configuration')
        config = Configuration(1)

        if not config.map_engine:
            raise UserError(gettext(
                'party_maps.missing_maps_engine'))
        geocoder_engine = getattr(cls, 'geocoder_%s' % config.map_engine)

        to_write = []
        for address in addresses:
            location = geocoder_engine(address, config)
            if location:
                map_place, (latitude, longitude) = location
                to_write.extend(([address], {
                    'latitude': latitude,
                    'longitude': longitude,
                    'map_place': map_place,
                    }))
        if to_write:
            cls.write(*to_write)

    def get_geocoder_address(self):
        if self.map_place:
            return self.map_place
        return '%s %s %s' % (self.street, self.zip, self.city)

    @classmethod
    def geocoder_googlemaps(cls, address, config):
        # try/except
        # GeocoderQuotaExceeded: The given key has gone over the requests limit
        # in the 24 hour period or has submitted too many requests in too
        # short a period of time.
        try:
            geolocator = geocoders.GoogleV3(
                api_key=config.map_engine_googlemaps_key)
            return geolocator.geocode('%s' % address.get_geocoder_address())
        except:
            return

    @classmethod
    def geocoder_openstreetmaps(cls, address, config):
        config.map_engine_openstreetmaps_agent = 'my-application'
        import geopy
        geopy.geocoders.options.default_timeout = 200
        geolocator = geocoders.Nominatim(
            user_agent=config.map_engine_openstreetmaps_agent)
        return geolocator.geocode('%s' % address.get_geocoder_address())

    @classmethod
    def map_url_googlemaps(cls, url):
        lang = Transaction().language[:2]
        return 'http://maps.google.com/maps?hl=%s&q=%s' % (lang, url)

    @classmethod
    def map_url_openstreetmaps(cls, url):
        return 'https://www.openstreetmap.org/search?query=%s' % url

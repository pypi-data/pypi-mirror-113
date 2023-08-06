# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['Configuration']


class Configuration(metaclass=PoolMeta):
    __name__ = 'party.configuration'
    map_engine = fields.Selection([
            ('googlemaps', 'Google Maps'),
            ('openstreetmaps', 'OpenStreetMap'),
            ],
        'Maps Engine')
    map_engine_googlemaps_key = fields.Char('Google Maps API Key',
        states={
            'invisible': Eval('map_engine') != 'googlemaps',
            },
        depends=['map_engine'])
    map_engine_openstreetmaps_agent = fields.Char('OpenStreetMaps User Agent',
        states={
            'invisible': Eval('map_engine') != 'openstreetmaps',
            'required': Eval('map_engine') == 'openstreetmaps',
            },
        depends=['map_engine'])

    @staticmethod
    def default_map_engine():
        return 'openstreetmaps'

    @staticmethod
    def default_map_engine_openstreetmaps_agent():
        return 'my-application'

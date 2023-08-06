# -*- coding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import json
from trytond.pool import PoolMeta


class Configuration(metaclass=PoolMeta):
    __name__ = 'elasticsearch.configuration'

    @classmethod
    def default_settings(cls):
        '''
        elastic_search
        - Set the path for the nicknames file on the LXC container
        '''
        settings = {
            "analysis": {
                "filter": {
                    "name_ngrams": {
                        "max_gram": 10,
                        "type": "edgeNGram",
                        "side": "front",
                        "min_gram": 1
                    },
                    "name_synonyms": {
                        "synonyms_path": "/etc/elasticsearch/synonyms/nicknames.txt",
                        "type": "synonym"
                    },
                    "name_metaphone": {
                        "replace": False,
                        "type": "phonetic",
                        "encoder": "metaphone"
                    }
                },
                "analyzer": {
                    "name_metaphone": {
                        "filter": [
                            "name_metaphone"
                        ],
                        "type": "custom",
                        "tokenizer": "standard"
                    },
                    "full_name": {
                        "filter": [
                            "standard",
                            "lowercase",
                            "asciifolding"
                        ],
                        "type": "custom",
                        "tokenizer": "standard"
                    },
                    "partial_name": {
                        "filter": [
                            "standard",
                            "lowercase",
                            "asciifolding",
                            "name_synonyms",
                            "name_ngrams"
                        ],
                        "type": "custom",
                        "tokenizer": "standard"
                    },
                    "html_analyzer": {
                        "type": "custom",
                        "tokenizer": "standard",
                        "char_filter": [
                            "html_strip"
                        ]
                    }
                }
            }
        }
        return json.dumps(settings, indent=4)

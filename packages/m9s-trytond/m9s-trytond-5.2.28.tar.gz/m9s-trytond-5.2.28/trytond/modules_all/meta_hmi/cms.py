# -*- coding: utf-8 -*-
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.cache import Cache


class Article(metaclass=PoolMeta):
    __name__ = 'nereid.cms.article'

    @classmethod
    def __setup__(cls):
        '''
        nereid_cms
          - Use the title instead of uri as rec_name
        '''
        super(Article, cls).__setup__()
        cls._rec_name = 'title'

    '''
    Set a cache for article menuitems to speedup the menu creation
    Note: this one seems to be used rarely or not
    '''
    _article_menuitem_cache = Cache('nereid.cms.article', context=False)

    @classmethod
    def clear_article_menuitem_cache(cls, *args):
        '''
        A method which conveniently clears the cache
         - used in triggers
        '''
        cls._article_menuitem_cache.clear()

    def get_menu_item(self, max_depth):
        cache_rv = self._article_menuitem_cache.get(self.id)
        if cache_rv is not None:
            return cache_rv
        res = super(Article, self).get_menu_item(max_depth)
        self._article_menuitem_cache.set(self.id, res)
        return res


class MenuItem(metaclass=PoolMeta):
    __name__ = 'nereid.cms.menuitem'

    '''
    Set a cache for menuitem menuitems to speedup the menu creation
    '''
    _menuitem_menuitem_cache = Cache('nereid.cms.menuitem', context=False)

    @classmethod
    def clear_menuitem_menuitem_cache(cls, *args):
        '''
        A method which conveniently clears the cache
         - used in triggers
        '''
        cls._menuitem_menuitem_cache.clear()

    def get_menu_item(self, max_depth):
        cache_rv = self._menuitem_menuitem_cache.get(self.id)
        if cache_rv is not None:
            return cache_rv
        res = super(MenuItem, self).get_menu_item(max_depth)
        self._menuitem_menuitem_cache.set(self.id, res)
        return res

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from sql.operators import NotILike


__all__ = ['Product']


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'
    
    attributes_string = fields.Function(fields.Char('Attributes'),
        'get_attributes_string', searcher='search_attributes_string')

    @classmethod
    def get_attributes_string(cls, products, name):
        result = {}.fromkeys([x.id for x in products], '')
        for product in products:
            if not product.attributes:
                continue
            result[product.id] = ','.join(['%s:%s' % (key, value)
                    for key, value in product.attributes.items()])
        return result

    @classmethod
    def search_attributes_string(cls, name, clause):
        Product = Pool().get('product.product')
        product = Product.__table__()

        # search product attributes in text plain (not dict) (keys and values)
        # Support ilike and not ilike opperators
        # Examples:
        # Attributes: Nan
        # Attributes: !Nan

        if clause[1] == 'not ilike':
            where = NotILike(product.attributes, clause[2])
        else:
            where = product.attributes.ilike(clause[2])
        query = product.select(product.id, where=where)

        return [('id', 'in', query)]

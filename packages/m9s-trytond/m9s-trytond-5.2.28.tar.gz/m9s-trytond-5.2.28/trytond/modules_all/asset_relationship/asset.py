# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from sql import Union, As, Column, Null
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelSQL, ModelView, fields
from trytond.transaction import Transaction
from trytond.pyson import If, Eval

__all__ = ['Asset', 'RelationType', 'AssetRelation', 'AssetRelationAll']


class Asset(metaclass=PoolMeta):
    __name__ = 'asset'
    relations = fields.One2Many('asset.relation.all', 'from_', 'Relations')


class RelationType(ModelSQL, ModelView):
    'Asset Relation Type'
    __name__ = 'asset.relation.type'

    name = fields.Char('Name', required=True, translate=True)
    reverse = fields.Many2One('asset.relation.type', 'Reverse Relation')


class AssetRelation(ModelSQL):
    'Asset Relation'
    __name__ = 'asset.relation'

    from_ = fields.Many2One('asset', 'From', required=True, select=True,
        ondelete='CASCADE')
    to = fields.Many2One('asset', 'To', required=True, select=True,
        ondelete='CASCADE')
    type = fields.Many2One('asset.relation.type', 'Type', required=True,
        select=True)
    company = fields.Many2One('company.company', 'Company', required=True,
        domain=[
            ('id', If(Eval('context', {}).contains('company'), '=', '!='),
                Eval('context', {}).get('company', -1)),
            ],
        select=True)

    @classmethod
    def __register__(cls, module_name):
        Asset = Pool().get('asset')

        asset_table = Asset.__table__()
        sql_table = cls.__table__()

        super(AssetRelation, cls).__register__(module_name)
        cursor = Transaction().connection.cursor()

        # update asset relation that not have the company
        sub_query = sql_table.join(asset_table,
                    condition=sql_table.from_ == asset_table.id
                    ).select(sql_table.id, asset_table.company,
                    where=(sql_table.company == Null))
        cursor.execute(*sub_query)

        for relation_id, company_id in cursor.fetchall():
            query = sql_table.update([sql_table.company], [company_id],
                where=sql_table.id == relation_id)
            cursor.execute(*query)

    @staticmethod
    def default_company():
        return Transaction().context.get('company')


class AssetRelationAll(AssetRelation, ModelView):
    'Asset Relation All'
    __name__ = 'asset.relation.all'

    @classmethod
    def table_query(cls):
        pool = Pool()
        Relation = pool.get('asset.relation')
        Type = pool.get('asset.relation.type')

        relation = Relation.__table__()
        type = Type.__table__()

        tables = {
            None: (relation, None)
            }
        reverse_tables = {
            None: (relation, None),
            'type': {
                None: (type, (relation.type == type.id) &
                    (type.reverse != Null)),
                },
            }

        company_id = Transaction().context.get('company')

        columns = []
        reverse_columns = []
        for name, field in Relation._fields.items():
            if hasattr(field, 'get'):
                continue
            column, reverse_column = cls._get_column(tables, reverse_tables,
                name)
            columns.append(column)
            reverse_columns.append(reverse_column)

        def convert_from(table, tables):
            right, condition = tables[None]
            if table:
                table = table.join(right, condition=condition)
            else:
                table = right
            for k, sub_tables in tables.items():
                if k is None:
                    continue
                table = convert_from(table, sub_tables)
            return table

        query = convert_from(None, tables).select(*columns,
            where=(relation.company == company_id))
        reverse_query = convert_from(None, reverse_tables).select(
            *reverse_columns)
        return Union(query, reverse_query, all_=True)

    @classmethod
    def _get_column(cls, tables, reverse_tables, name):
        table, _ = tables[None]
        reverse_table, _ = reverse_tables[None]
        if name == 'id':
            return As(table.id * 2, name), As(reverse_table.id * 2 + 1, name)
        elif name == 'from_':
            return table.from_, reverse_table.to.as_(name)
        elif name == 'to':
            return table.to, reverse_table.from_.as_(name)
        elif name == 'type':
            reverse_type, _ = reverse_tables[name][None]
            return table.type, reverse_type.reverse.as_(name)
        else:
            return Column(table, name), Column(reverse_table, name)

    @staticmethod
    def convert_instances(relations):
        "Converts asset.relation.all instances to asset.relation "
        pool = Pool()
        Relation = pool.get('asset.relation')
        return Relation.browse([x.id // 2 for x in relations])

    @property
    def reverse_id(self):
        if self.id % 2:
            return self.id - 1
        else:
            return self.id + 1

    @classmethod
    def create(cls, vlist):
        pool = Pool()
        Relation = pool.get('asset.relation')
        relations = Relation.create(vlist)
        return cls.browse([r.id * 2 for r in relations])

    @classmethod
    def write(cls, all_records, values):
        pool = Pool()
        Relation = pool.get('asset.relation')

        # Increase transaction counter
        Transaction().counter += 1

        # Clean local cache
        for record in all_records:
            for record_id in (record.id, record.reverse_id):
                local_cache = record._local_cache.get(record_id)
                if local_cache:
                    local_cache.clear()

        # Clean cursor cache
        for cache in Transaction().connection.cursor().cache.values():
            if cls.__name__ in cache:
                for record in all_records:
                    for record_id in (record.id, record.reverse_id):
                        if record_id in cache[cls.__name__]:
                            cache[cls.__name__][record_id].clear()

        reverse_values = values.copy()
        if 'from_' in values and 'to' in values:
            reverse_values['from_'], reverse_values['to'] = \
                reverse_values['to'], reverse_values['from_']
        elif 'from_' in values:
            reverse_values['to'] = reverse_values.pop('from_')
        elif 'to' in values:
            reverse_values['from_'] = reverse_values.pop('to')
        straight_relations = [r for r in all_records if not r.id % 2]
        reverse_relations = [r for r in all_records if r.id % 2]
        if straight_relations:
            Relation.write(cls.convert_instances(straight_relations),
                values)
        if reverse_relations:
            Relation.write(cls.convert_instances(reverse_relations),
                reverse_values)

    @classmethod
    def delete(cls, relations):
        pool = Pool()
        Relation = pool.get('asset.relation')

        # Increase transaction counter
        Transaction().counter += 1

        # Clean cursor cache
        for cache in list(Transaction().cache.values()):
            for cache in (cache, list(cache.get('_language_cache', {}).values())):
                if cls.__name__ in cache:
                    for record in relations:
                        for record_id in (record.id, record.reverse_id):
                            if record_id in cache[cls.__name__]:
                                del cache[cls.__name__][record_id]

        Relation.delete(cls.convert_instances(relations))

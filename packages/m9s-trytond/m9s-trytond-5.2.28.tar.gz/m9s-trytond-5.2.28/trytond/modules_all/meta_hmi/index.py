# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from pyes.exceptions import NotFoundException
from trytond.pool import PoolMeta, Pool


class IndexBacklog(metaclass=PoolMeta):
    __name__ = 'elasticsearch.index_backlog'

    @classmethod
    def update_index(cls, batch_size=1000):
        '''
        elastic_search

        Complete override
        - Our LXC container can handle 1000 requests per min
          (with a cron run every 5 min this should be safe)
        - Clean any products with displayed_on_eshop == False from the index
          we use the index only for the web search (#2684).
        '''
        config = Pool().get('elasticsearch.configuration')(1)

        conn = config.get_es_connection()
        index_name = config.index_name

        for item in cls.search_read(
                [], order=[('id', 'DESC')], limit=batch_size,
                fields_names=['record_model', 'record_id', 'id']):

            Model = Pool().get(item['record_model'])

            doc_type = config.make_type_name(Model.__name__)
            record_id = item['record_id']

            do_index = True
            try:
                record, = Model.search([('id', '=', item['record_id'])])
                if hasattr(record, 'displayed_on_eshop'):
                    if not record.displayed_on_eshop:
                        do_index = False
                        cls.delete_from_index(conn, index_name, doc_type,
                            record_id)
            except ValueError:
                # Record may have been deleted in the meantime
                cls.delete_from_index(conn, index_name, doc_type, record_id)
            else:
                if do_index:
                    if hasattr(record, 'elastic_search_json'):
                        # A model with the elastic_search_json method
                        data = record.elastic_search_json()
                    else:
                        # A model without elastic_search_json
                        data = cls._build_default_doc(record)

                    conn.index(data, index_name, doc_type, record.id)
            finally:
                # Delete the item since it has been sent to the index
                cls.delete([cls(item['id'])])

    @staticmethod
    def delete_from_index(conn, index, doc_type, record_id):
        try:
            conn.delete(index, doc_type, record_id)
        except NotFoundException:
            pass

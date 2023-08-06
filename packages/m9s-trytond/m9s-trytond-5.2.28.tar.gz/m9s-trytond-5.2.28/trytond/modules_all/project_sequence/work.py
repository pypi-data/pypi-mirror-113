# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction

__all__ = ['Work']

class Work(metaclass=PoolMeta):
    __name__ = 'project.work'

    code = fields.Char('Code', readonly=True, select=True)

    def get_rec_name(self, name):
        transaction = Transaction()
        with transaction.set_context(rec_name_without_code=True):
            res = super(Work, self).get_rec_name(name)
        if (self.code and
                not transaction.context.get('rec_name_without_code', False)):
            return '[%s] %s' % (self.code, res)
        return res

    @classmethod
    def search_rec_name(cls, name, clause):
        domain = super(Work, cls).search_rec_name(name, clause)
        return ['OR',
            domain,
            ('code',) + tuple(clause[1:]),
            ]

    @classmethod
    def create(cls, vlist):
        Sequence = Pool().get('ir.sequence')
        Configuration = Pool().get('work.configuration')

        vlist = [x.copy() for x in vlist]
        for values in vlist:
            if not values.get('code'):
                config = Configuration(1)
                if not config.work_sequence:
                    continue
                values['code'] = Sequence.get_id(config.work_sequence.id)
        return super(Work, cls).create(vlist)

    @classmethod
    def copy(cls, works, default=None):
        if default is None:
            default = {}
        if 'code' not in default:
            default['code'] = None
        return super(Work, cls).copy(works, default)

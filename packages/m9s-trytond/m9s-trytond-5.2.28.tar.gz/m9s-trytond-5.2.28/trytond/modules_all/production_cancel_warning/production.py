# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.model import ModelView, Workflow
from trytond.pool import PoolMeta, Pool
from trytond.i18n import gettext
from trytond.exceptions import UserWarning

__all__ = ['Production']


class Production(metaclass=PoolMeta):
    __name__ = 'production'

    @classmethod
    @ModelView.button
    @Workflow.transition('cancel')
    def cancel(cls, productions):
        Warning = Pool().get('res.user.warning')
        for production in productions:
            key = 'are_you_sure_%d' % production.id
            if Warning.check(key):
                raise UserWarning(key, gettext(
                    'production_cancel_warning.are_you_sure',
                    production=production.number))
        super(Production, cls).cancel(productions)

# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

from trytond.pool import PoolMeta


class User(metaclass=PoolMeta):
    __name__ = 'res.user'

    @classmethod
    def _login_none(cls, login, parameters):
        user_id, _, _ = cls._get_login(login)
        if user_id:
            return user_id

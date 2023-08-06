# This file is part of Coog. The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
import logging
import sys
import traceback

from werkzeug.exceptions import HTTPException

from trytond.config import config
from trytond.exceptions import TrytonException, UserError
from trytond.transaction import Transaction

logger = logging.getLogger(__name__)

sentry_dsn = config.get('sentry', 'dsn')
sentry_log_user = config.get('sentry', 'log_user')
sentry_lang = config.get('sentry', 'lang', default='en')


def sentry_wrap(func):

    def wrap(*args, **kwargs):
        with sentry_sdk.push_scope() as scope:
            #scope.set_extra('debug', False)
            try:
                return func(*args, **kwargs)
            except (TrytonException, HTTPException):
                raise
            except Exception as e:
                ex_type, ex, tb = sys.exc_info()
                #language = Transaction().language
                #print(dir(Transaction()))
                #print(Transaction().user)
                #print(Transaction().database)
                #try:
                #    print(Transaction().language)
                #except:
                #    pass
                #print(dir(Transaction().connection.cursor()))
                #print(Transaction().context)
                #username = request.authorization.username
                #print('un', username)
                data = {
                    'exception_type': str(type(e)),
                    'exception_args': e.args,
                    'formatted_exception': traceback.format_exception(type(e), e, tb),
                    'root_directory': sys.path[0],
                    }
                #event_id = sentry_sdk.capture_exception(e)
                if sentry_log_user:
                    from trytond.pool import Pool
                    try:
                        pool = Pool()
                    except Exception:
                        pool = None
                    if pool:
                        try:
                            User = pool.get('res.user')
                            tryton_user = User(data['user_id'])
                            tryton_user = User(Transaction['user'])
                            data.update({
                                'user_name': tryton_user.rec_name,
                                'user_login': tryton_user.login,
                                'user_email': tryton_user.email,
                                })
                            set_user({'username': tryton_user.rec_name})
                        except Exception:
                            pass
                sentry_sdk.set_context('state', data)
                #scope.set_extra(data)
                scope.set_extra('user_name', 'jojo')
                set_user({'username': 'waldfee'})
                print('d', data)
                event_id = sentry_sdk.capture_exception(e)
                raise UserError(
                    'An error occured\n\n'
                    'Maintenance has been notified of this failure.\n'
                    'In case you wish to discuss this issue with the team, please '
                    'provide the following reference :\n\n%s' % event_id
                    )
    if sentry_dsn:
        logger.info('setting sentry: %s' % sentry_dsn)
        import sentry_sdk
        from sentry_sdk import set_user
        sentry_sdk.init(sentry_dsn)
        return wrap
    else:
        return func

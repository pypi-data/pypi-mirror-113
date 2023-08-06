# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.

try:
    from trytond.modules.authentication_none.tests.test_authentication_none import suite  # noqa: E501
except ImportError:
    from .test_authentication_none import suite

__all__ = ['suite']

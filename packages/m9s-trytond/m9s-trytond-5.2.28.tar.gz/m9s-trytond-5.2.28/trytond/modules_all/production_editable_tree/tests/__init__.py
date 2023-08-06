# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
try:
    from trytond.modules.production_editable_tree.tests.test_production_editable_tree import suite
except ImportError:
    from .test_production_editable_tree import suite

__all__ = ['suite']

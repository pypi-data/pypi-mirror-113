#The COPYRIGHT file at the top level of this repository contains the full
#copyright notices and license terms.
from trytond.model import fields, ModelView
from trytond.pool import PoolMeta
from trytond.modules.jasper_reports.jasper import JasperReport

__all__ = ['Move', 'MoveLabel']


class Move(metaclass=PoolMeta):
    __name__ = 'stock.move'
    label_party = fields.Function(fields.Many2One('party.party', 'Party'),
        'get_label_party')
    label_use_date = fields.Function(fields.Date('Use date'),
        'get_label_use_date')

    @classmethod
    def __setup__(cls):
        super(Move, cls).__setup__()
        cls._buttons.update({
                'print_label': {},
                })

    def get_label_party(self, name):
        value = None
        if self.shipment:
            for name in ('supplier', 'customer', 'party'):
                if hasattr(self.shipment, name):
                    value = getattr(self.shipment, name)
        if value:
            return value.id

    def get_label_use_date(self, name):
        if hasattr(self, 'lot') and hasattr(self.lot, 'expiry_date'):
            return self.lot.expiry_date

    @classmethod
    @ModelView.button_action('stock_move_label.report_stock_move_label')
    def print_label(cls, moves):
        pass


class MoveLabel(JasperReport):
    __name__ = 'stock.move.label'

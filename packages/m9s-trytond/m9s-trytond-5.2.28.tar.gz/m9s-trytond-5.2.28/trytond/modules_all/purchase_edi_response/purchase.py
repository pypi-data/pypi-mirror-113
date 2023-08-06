# -*- coding: utf-8 -*
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields, ModelSQL, ModelView
from trytond.pool import PoolMeta, Pool
from trytond.pyson import Eval, Bool, Or
import os
from trytond.transaction import Transaction
from trytond.modules.purchase_edi.purchase import DATE_FORMAT
from trytond.modules.product import price_digits
from trytond.i18n import gettext
from trytond.exceptions import UserError
import datetime
from edifact.message import Message
from edifact.control import Characters
from edifact.serializer import Serializer
from edifact.utils import (with_segment_check,
    separate_section, RewindIterator, DO_NOTHING, NO_ERRORS)
import oyaml as yaml
from io import open
import copy
from decimal import Decimal


__all__ = ['Purchase', 'PurchaseConfiguration', 'PurchaseLine',
    'EdiOrderResponseLine']


DEFAULT_FILES_LOCATION = '/tmp/'

# EDI to Tryton UOMS mapping
UOMS_EDI_TO_TRYTON = {
    'KGM': 'kg',
    'PCE': 'u',
    'LTR': 'l',
    'GRM': 'g',
    'MTR': 'm',
}
MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = 'ORDRSP_ediversa.yml'
KNOWN_EXTENSIONS = ['.txt', '.edi', '.pla']


def get_datetime_obj_from_edi_date(edi_date):
    return datetime.datetime.strptime(edi_date, DATE_FORMAT)


class Purchase(metaclass=PoolMeta):
    __name__ = 'purchase.purchase'

    edi_answered_state = fields.Selection([
        (None, ''),
        ('4', 'change'),
        ('12', 'not process'),
        ('27', 'not accepted'),
        ('29', 'Accepted')], 'EDI Response State', states={
            'readonly': True,
            'invisible': ~Eval('edi_state').in_(['answered'])
            })
    edi_answered_on = fields.DateTime('Answered On', states={
            'readonly': True,
            'invisible': ~Eval('edi_state').in_(['answered'])
            })
    edi_response_lines_to_review = fields.Function(
        fields.One2Many('purchase.edi.order.response.lin', None,
            'Response Lines', states={
                'invisible': ~Eval('edi_state').in_(['answered'])
                }, depends=['edi_state']),
        'get_edi_response_lines_from_purchase_lines')
    edi_response_delivery_date = fields.DateTime('EDI Response Delivery Date',
        states={
            'readonly': True,
            'invisible': ~Eval('edi_state').in_(['answered'])
            })
    edi_base_amount = fields.Numeric('EDI Base Amount',
        states={
            'readonly': True,
            'invisible': ~Eval('edi_state').in_(['answered'])
            })
    edi_total_amount = fields.Numeric('EDI Total Amount',
        states={
            'readonly': True,
            'invisible': ~Eval('edi_state').in_(['answered'])
            })

    @classmethod
    def view_attributes(cls):
        return super(Purchase, cls).view_attributes() + [
            ('//separator[@id="response_msg"]', 'states', {
                    'invisible': (Or(
                            ~Bool(Eval('use_edi')),
                            ~Eval('edi_state').in_(['answered']))),
                    })]

    @classmethod
    def __setup__(cls):
        super(Purchase, cls).__setup__()
        cls.edi_state.selection.append(('answered', 'Answered'))
        cls._buttons.update({
            'get_edi_response': {
                'readonly': ~Eval('edi_state').in_(['sended']),
                'invisible': ~Eval('edi_state').in_(['sended'])
                }
            })

    @classmethod
    def copy(cls, purchases, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['edi_answered_state'] = None
        default['edi_answered_on'] = None
        default['edi_total_amount'] = None
        default['edi_base_amount'] = None
        default['edi_response_delivery_date'] = None
        return super(Purchase, cls).copy(purchases, default=default)

    def get_edi_response_lines_from_purchase_lines(self, name=None):
        return [l.edi_response.id for l in self.lines if l.edi_response and
                l.edi_response.state not in ['1', '5']]

    @staticmethod
    def set_control_chars(template_control_chars):
        cc = Characters()
        cc.data_separator = template_control_chars.get('data_separator',
            cc.data_separator)
        cc.segment_terminator = template_control_chars.get(
            'segment_terminator', cc.segment_terminator)
        cc.component_separator = template_control_chars.get(
            'component_separator', cc.component_separator)
        cc.decimal_point = template_control_chars.get('decimal_point',
            cc.decimal_point)
        cc.escape_character = template_control_chars.get('escape_character',
            cc.escape_character)
        cc.reserved_character = template_control_chars.get(
            'reserved_character', cc.reserved_character)
        return cc

    @classmethod
    def import_edi_response(cls, response, template, purchases=None):
        total_errors = []
        control_chars = cls.set_control_chars(
            template.get('control_chars', {}))
        message = Message.from_str(response.upper().replace('\r', ''),
            characters=control_chars)
        segments_iterator = RewindIterator(message.segments)
        template_header = template.get('header', {})
        # template_detail = template.get('detail', {})
        template_resume = template.get('resume', {})
        # detail = [x for x in separate_section(segments_iterator, start='LIN',
        #         end='MOARES')]
        del(segments_iterator)
        # If there isn't a segment ORDRSP_D_96A_UN_EAN005
        # means the file readed it's not a order response.
        if not message.get_segment('ORDRSP_D_96A_UN_EAN005'):
            return DO_NOTHING, NO_ERRORS
        template_header.pop('ORDRSP_D_96A_UN_EAN005', None)

        rff = message.get_segment('RFF')
        template_rff = template_header.get('RFF')
        purchase, errors = cls._process_RFF(rff, template_rff, control_chars)
        if errors:
            total_errors += errors
        if not purchase:
            return None, total_errors

        # Used if we want to import only a specific purchases
        if purchases:
            if purchase not in purchases:
                return DO_NOTHING, NO_ERRORS

        purchase.edi_state = 'answered'
        template_header.pop('RFF')

        dtm = message.get_segment('DTM')
        template_dtm = template_header.get('DTM')
        edi_answered_on, errors = cls._process_DTM(dtm, template_dtm,
            control_chars)
        if errors:
            total_errors += errors
        purchase.edi_answered_on = edi_answered_on or datetime.datetime.now()

        bgm = message.get_segment('BGM')
        template_bgm = template_header.get('BGM')
        edi_answered_state, errors = cls._process_BGM(bgm, template_bgm,
            control_chars)
        if errors:
            total_errors += errors
        purchase.edi_answered_state = edi_answered_state

        # This action is deactivated in order to know if it's necessary
        # for the client

        # if purchase.edi_answered_state != '29':
        #     for linegroup in detail:
        #         edi_line = EdiOrderResponseLine()
        #         for segment in linegroup:
        #             if segment.tag not in template_detail.keys():
        #                 continue
        #             template_segment = template_detail.get(segment.tag)
        #             process = eval('cls._process_{}'.format(segment.tag))
        #             to_update, errors = process(segment, template_segment)
        #             if errors:
        #                 # If there are errors the linegroup isn't processed
        #                 total_errors += errors
        #                 break
        #             if to_update:
        #                 values.update(to_update)
        #         if errors:
        #             continue

        moares = message.get_segment('MOARES')
        template_moares = template_resume.get('MOARES', None)
        if moares and template_moares:
            values, errors = cls._process_MOARES(
                moares, template_moares, control_chars)
            if errors:
                total_errors += errors
            else:
                purchase.edi_base_amount = values.get('base_amount')
                purchase.edi_total_amount = values.get('total_amount')

        return purchase, total_errors

    @classmethod
    @with_segment_check
    def _process_RFF(cls, segment, template_segment, control_chars=None):
        pool = Pool()
        Purchase = pool.get('purchase.purchase')
        purchase_num = segment.elements[1]
        purchase = Purchase.search([
                ('number', '=', purchase_num),
                ('state', '=', 'confirmed'),
                ('edi_state', '=', 'sended')], limit=1)
        if not purchase:
            error_msg = 'Purchase number {} not found'.format(purchase_num)
            serialized_segment = Serializer(control_chars).serialize([segment])
            return DO_NOTHING, ['{}: {}'.format(error_msg, serialized_segment)]
        purchase, = purchase
        return purchase, NO_ERRORS

    @classmethod
    @with_segment_check
    def _process_DTM(cls, segment, template, control_chars=None):
        edi_answered_on = get_datetime_obj_from_edi_date(segment.elements[0])
        return edi_answered_on, NO_ERRORS

    @classmethod
    @with_segment_check
    def _process_BGM(cls, segment, template, control_chars=None):
        return segment.elements[2], NO_ERRORS

    @classmethod
    @with_segment_check
    def _process_MOARES(cls, segment, template, control_chars=None):
        elements = segment.elements
        return {'base_amount': Decimal(elements[0]) if len(elements) else None,
                'total_amount': Decimal(elements[1]) if len(elements) > 1 else
                None}, NO_ERRORS

    @classmethod
    def import_edi_responses(cls, purchases=None):
        pool = Pool()
        Configuration = pool.get('purchase.configuration')
        configuration = Configuration(1)
        source_path = os.path.abspath(configuration.inbox_path_edi or
            DEFAULT_FILES_LOCATION)
        files = [os.path.join(source_path, fp) for fp in
                 os.listdir(source_path) if os.path.isfile(os.path.join(
                     source_path, fp))]
        files_to_delete = []
        errors_path = os.path.abspath(configuration.errors_path_edi or
            DEFAULT_FILES_LOCATION)
        template_name = configuration.template_response_edi or DEFAULT_TEMPLATE
        template_path = os.path.join(os.path.join(MODULE_PATH, 'templates'),
            template_name)
        with open(template_path, encoding='utf-8') as fp:
            template = yaml.load(fp.read())
        to_write = []
        result = []
        for fname in files:
            if fname[-4:].lower() not in KNOWN_EXTENSIONS:
                continue
            with open(fname, 'rb') as fp:
                response = fp.read()
            try:
                response = response.encode('utf-8')
                purchase, errors = cls.import_edi_response(response,
                    copy.deepcopy(template), purchases)
            except RuntimeError:
                continue
            else:
                basename = os.path.basename(fname)
                if purchase:
                    with Transaction().set_user(0, set_context=True):
                        purchase.add_attachment(response, basename)
                    to_write.extend(([purchase], purchase._save_values))
                    files_to_delete.append(fname)
                if errors:
                    error_fname = os.path.join(
                        errors_path,
                        'error_{}.EDI'.format(os.path.splitext(basename)[0]))
                    with open(error_fname, 'w') as fp:
                        fp.write('\n'.join(errors))
        if to_write:
            cls.write(*to_write)
            result = to_write[0]
        if files_to_delete:
            for file in files_to_delete:
                os.remove(file)
        to_process = cls.search([
            ('edi_answered_state', '=', '29'),
            ('state', '=', 'confirmed')])
        if to_process:
            cls.process(to_process)

        return result

    @classmethod
    def update_edi_orders_state(cls):
        super(Purchase, cls).update_edi_orders_state()
        cls.import_edi_responses()

    @classmethod
    @ModelView.button
    def get_edi_response(cls, purchases):
        result = cls.import_edi_responses(purchases)
        without_response = list(set(purchases) - set(result))
        for purchase in without_response:
            raise UserError(gettext('no_edi_response', num=purchase.number))


class PurchaseLine(metaclass=PoolMeta):
    __name__ = 'purchase.line'

    edi_response = fields.One2Many('purchase.edi.order.response.lin', 'line',
        'EDI Response Line', states={'readonly': True})

    @classmethod
    def copy(cls, lines, default=None):
        if default is None:
            default = {}
        default = default.copy()
        default['edi_response'] = None
        return super(PurchaseLine, cls).copy(lines, default=default)


class EdiOrderResponseLine(ModelView, ModelSQL):
    'EDI ORDER Response Line'
    __name__ = 'purchase.edi.order.response.lin'

    line = fields.Many2One('purchase.line', 'Line',
        states={'readonly': True})
    description = fields.Text('Description', size=None,
        states={'readonly': True})
    changes_applied = fields.Boolean('EDI Changes Applied', states={
            'invisible': True,
            })
    product = fields.Function(fields.Many2One('product.product', 'Product'),
        'get_product')
    code = fields.Char('Code', states={'readonly': True})
    line_code = fields.Char('Line Code', states={'readonly': True})
    state = fields.Selection([
            ('1', 'Added'),
            ('3', 'Changed'),
            ('5', 'Accepted'),
            ('7', 'Not accepted'),
            ('6', 'Accepted with Correction')],
        'State', states={'readonly': True})
    quantity = fields.Float('Quantity',
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'],
        states={'readonly': True})
    quantity_on_stock = fields.Numeric('Quantity On Stock',
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'],
        states={'readonly': True})
    quantity_not_served = fields.Numeric('Quantity Not Served',
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'],
        states={'readonly': True})
    unit = fields.Many2One('product.uom', 'Uom', states={
            'readonly': True}, ondelete='RESTRICT')
    unit_digits = fields.Function(fields.Integer('Unit Digits', states={
            'invisible': True,
            'readonly': True}), 'on_change_with_unit_digits')
    base_amount = fields.Numeric('Base Amount', digits=price_digits, states={
            'readonly': True})
    total = fields.Numeric('Total', digits=price_digits, states={
            'readonly': True})
    cause = fields.Selection([  # motivo #QVRLIN)
            ('AA', 'Product written off by the wholesaler'),
            ('AB', 'Product that has been left to manufacture'),
            ('AD', 'Product without factory stock'),
            ('AS', 'Available now - planned shipment'),
            ('BK', 'Supplementary delivery of a previous order'),
            ('BP', 'Partial shipment that will be followed by a ' \
                'complementary shipment'),
            ('CP', 'Partial shipment considered complete without ' \
                'supplementary shipment'),
            ('CN', 'Next carrier'),
            ('PS', 'In process-planned shipment'),
            ('OS', 'Product sold out due to force majeure'),
            ('OW', 'Exhausted item in the wholesaler'),
            ('TW', 'Product temporarily unavailable by the wholesaler')
            ], 'Cause', states={'readonly': True})
    reason = fields.Selection([  # razon #QVRLIN)
            ('ADJ', 'Adjustment'),
            ('AUE', 'Unknown product code'),
            ('AV', 'Out of inventory'),
            ('AQ', 'Quantity and Unit of Measure Alternatives'),
            ('IS', 'The order represents a replacement of the original order'),
            ('PC', 'Pack difference'),
            ('UM', 'Unit of measure difference'),
            ('WV', 'The amount requested doesn\'t match the agreement')
            ], 'Reason', states={'readonly': True})
    price = fields.Numeric('Price', digits=price_digits, states={
            'readonly': True})  # PRILIN precio
    quantity_by_price = fields.Float('Quantity by Price',  # PRILIN base
        digits=(16, Eval('unit_digits', 2)),
        depends=['unit_digits'],
        states={'readonly': True})
    delivery_date = fields.DateTime('Delivery Date', states={
            'readonly': True})

    # TODO: Apply changes to purchase lines
    # @classmethod
    # def __setup__(cls):
    #     super(EdiOrderResponseLine, cls).__setup__()
    #     cls._buttons.update({
    #         'apply_changes_to_purchase_line': {
    #             'invisible': ~Eval('state').in_([3, 6]),
    #             'readonly': Eval('changes_applied')
    #             }
    #         })

    # @classmethod
    # @ModelView.button
    # def apply_changes_to_purchase_line(cls, edi_lines):
    #     for edi_line in edi_lines:
    #         pass

    @staticmethod
    def get_tryton_unit(edi_unit):
        pool = Pool()
        Uom = pool.get('product.uom')
        uom = Uom.search([
                ('symbol', '=', UOMS_EDI_TO_TRYTON.get(edi_unit))
                ], limit=1)
        return uom[0] if uom else None

    @fields.depends('unit')
    def on_change_with_unit_digits(self, name=None):
        if self.unit:
            return self.unit.digits
        return 2

    def get_product(self, name):
        pass


class PurchaseConfiguration(metaclass=PoolMeta):
    __name__ = 'purchase.configuration'

    inbox_path_edi = fields.Char('Inbox Path EDI')
    errors_path_edi = fields.Char('Errors Path')
    template_response_edi = fields.Char('Template EDI Used for Response')

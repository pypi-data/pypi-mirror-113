# This file is part product_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval, Not, Bool
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['Attachment']
STATES = {
    'invisible': ~Eval('esale_available', True),
    }
DEPENDS = ['esale_available']


class Attachment(metaclass=PoolMeta):
    __name__ = 'ir.attachment'
    esale_available  = fields.Boolean('Available eSale',
        help='This image are available in your e-commerce.')
    esale_base_image = fields.Boolean('Base Image', states=STATES,
        depends=DEPENDS)
    esale_small_image = fields.Boolean('Small Image', states=STATES,
        depends=DEPENDS)
    esale_thumbnail = fields.Boolean('Thumbnail Image', states=STATES,
        depends=DEPENDS)
    esale_exclude = fields.Boolean('Exclude', states=STATES,
        depends=DEPENDS,
        help='Defines whether the image will associate only to one of '
            'three image types ')
    esale_position = fields.Integer('Position', states=STATES,
        depends=DEPENDS,
        help='Image file position ')
    esale_label = fields.Char('eSale Label', translate=True)

    @classmethod
    def __setup__(cls):
        super(Attachment, cls).__setup__()
        cls._order.insert(0, ('esale_position', 'ASC'))
        cls._order.insert(1, ('id', 'ASC'))

    @staticmethod
    def default_esale_base_image():
        return True

    @staticmethod
    def default_esale_small_image():
        return True

    @staticmethod
    def default_esale_thumbnail():
        return True

    @staticmethod
    def default_esale_position():
        return 1

    @classmethod
    def delete(cls, attachments):
        for attachment in attachments:
            if attachment.esale_available:
                raise UserError(gettext(
                    'product_esale.delete_esale_attachment',
                        attachment=attachment.rec_name))
        super(Attachment, cls).delete(attachments)

    @classmethod
    def view_attributes(cls):
        return super(Attachment, cls).view_attributes() + [
            ('//page[@id="esale"]', 'states', {
                    'invisible': Not(Bool(Eval('esale_available'))),
                    })]

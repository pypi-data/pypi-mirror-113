# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.config import config as config_
from PIL import Image
import io

__all__ = ['Attachment', 'Template']
THUMB_QUALITY = config_.getint('product', 'thumb_quality', default=85)
THUMB_CROP = config_.get('product', 'thumb_crop', default='')
THUMB_WIDTH = config_.getint('product', 'thumb_width', default=600)
THUMB_HEIGHT = config_.getint('product', 'thumb_height', default=600)

class Attachment(metaclass=PoolMeta):
    __name__ = 'ir.attachment'
    product_image = fields.Boolean('Product Image')


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    images = fields.One2Many('ir.attachment', 'resource', 'Images',
        filter=[
            ('product_image', '=', True),
            ])
    image = fields.Function(fields.Many2One('ir.attachment', 'Image'),
        'get_image')
    image_thumb = fields.Function(fields.Binary('Image Thumb',
        filename='image_thumb_filename'), 'get_image_thumb')
    image_thumb_filename = fields.Function(fields.Char("File Name Image Thumb"),
        'get_image_thumb_filename')

    @classmethod
    def get_image(cls, records, names):
        res = {n: {r.id: None for r in records} for n in names}
        for name in names:
            for record in records:
                if record.images:
                    res[name][record.id] = record.images[0].id
        return res

    @staticmethod
    def thumb(data, image_format, crop=THUMB_CROP,
            width=THUMB_WIDTH, height=THUMB_HEIGHT, quality=THUMB_QUALITY):
        size = (width, height)
        try:
            img = Image.open(io.BytesIO(data))
        except:
            return

        if crop:
            img_ratio = img.size[0] / float(img.size[1])
            ratio = size[0] / float(size[1])

            # Scaled/cropped vertically or horizontally depending on the ratio
            if ratio > img_ratio:
                img = img.resize((size[0], size[0] * img.size[1] / img.size[0]),
                    Image.ANTIALIAS)
                # Crop in the top, middle or bottom
                if crop == 'top':
                    box = (0, 0, img.size[0], size[1])
                elif crop == 'bottom':
                    box = (0, img.size[1] - size[1], img.size[0], img.size[1])
                else :
                    box = (0, (img.size[1] - size[1]) / 2, img.size[0],
                        (img.size[1] + size[1]) / 2)
                img = img.crop(box)
            elif ratio < img_ratio:
                img = img.resize((size[1] * img.size[0] / img.size[1], size[1]),
                    Image.ANTIALIAS)
                # Crop in the top, middle or bottom
                if crop == 'top':
                    box = (0, 0, size[0], img.size[1])
                elif crop == 'bottom':
                    box = (img.size[0] - size[0], 0, img.size[0], img.size[1])
                else :
                    box = ((img.size[0] - size[0]) / 2, 0,
                        (img.size[0] + size[0]) / 2, img.size[1])
                img.crop(box)
        else:
            img.thumbnail(size)

        imgByteArr = io.BytesIO()
        img.save(imgByteArr, image_format, quality=quality)
        return bytearray(imgByteArr.getvalue())

    @classmethod
    def get_image_thumb(cls, records, names):
        res = {n: {r.id: None for r in records} for n in names}
        for name in names:
            for record in records:
                if record.image and record.image.data:
                    image_format, = record.image.name.split('.')[-1:]
                    imgformat = (image_format.lower() if image_format.lower()
                        in {'png', 'jpeg'} else 'jpeg')
                    res[name][record.id] = cls.thumb(record.image.data, imgformat)
        return res

    def get_image_thumb_filename(self, name):
        return self.image.name if self.image else None

    @classmethod
    def delete(cls, templates):
        pool = Pool()
        Attachment = pool.get('ir.attachment')

        attachments = [a for t in templates for a in t.images]
        Attachment.delete(attachments)
        super(Template, cls).delete(templates)

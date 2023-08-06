# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard, StateView, Button, StateAction
from trytond.transaction import Transaction
from trytond.pyson import PYSONEncoder, Bool, Eval, If
from trytond.pool import Pool, PoolMeta
from trytond.wizard import Wizard, StateView, StateTransition, Button
from trytond import backend
import codecs
from trytond.i18n import gettext
from trytond.exceptions import UserError, UserWarning


__all__ = ['ProductionBomOrcad', 'BOM']


class ProductionBomOrcad(ModelSQL, ModelView):
    "Product Bom Orcad"
    __name__ = 'production.bom.orcad'
    _rec_name = 'description'

    bom = fields.Many2One('production.bom', 'BOM', required=True,
        ondelete='CASCADE')
    product = fields.Many2One('product.product', 'Product')
    quantity = fields.Char('Quantity', readonly=True, required=True)
    reference = fields.Char('Reference')
    description = fields.Char('Description', readonly=True, required=True)
    part_number = fields.Char('Part number')

    @classmethod
    def __setup__(cls):
        super(ProductionBomOrcad, cls).__setup__()


class BOM(metaclass=PoolMeta):
    __name__ = 'production.bom'

    orcad_lines = fields.One2Many('production.bom.orcad',
        'bom', 'Orcad Importation')
    orcad_file = fields.Binary('Orcad File', filename='filename')
    filename = fields.Char('Filename')

    @classmethod
    def __setup__(cls):
        super(BOM, cls).__setup__()
        cls._buttons.update({
                'process_orcad_file': {
                    'readonly': ~Eval('orcad_file')
                    },
                'create_inputs': {
                    'readonly': (~Eval('orcad_lines') | Eval('inputs')
                        | Eval('state'))
                    },
                })

    @classmethod
    @ModelView.button
    def process_orcad_file(cls, records):
        Warning = Pool().get('res.user.warning')
        for record in records:
            if not record.orcad_file:
                raise UserError(gettext(
                    'production_bom_orcad_import.no_file'))
            values, res = record.search_products()
            # No values, incorrect file
            # res = False, some products nor found: values = products not found
            if not values:
                raise UserError(gettext(
                    'production_bom_orcad_import.incorrect_file'))
            elif not res:
                key = 'product_not_found_%s'%record.id
                if Warning.check(key):
                    raise UserWarning(key, gettext(
                        'production_bom_orcad_import.no_product'))
            record.load_values(values, res)

    @classmethod
    @ModelView.button
    def create_inputs(cls, records):
        pool = Pool()
        Orcad = pool.get('production.bom.orcad')
        Input = pool.get('production.bom.input')

        for record in records:
            orcads = Orcad.search([('bom', '=', record.id)])
            to_create = []
            for orcad in orcads:
                if not orcad.product:
                    raise UserError(gettext(
                        'production_bom_orcad_import.no_product'))
                else:
                    new_input = Input()
                    new_input.bom = record
                    new_input.product = orcad.product
                    new_input.quantity = orcad.quantity
                    new_input.uom = orcad.product.default_uom
                    new_input.map_distribution = orcad.reference
                    to_create.append(new_input)
            Input.create([x._save_values for x in to_create])

    def load_values(self, values, result):
        pool = Pool()
        Orcad = pool.get('production.bom.orcad')

        to_create = []

        for (quantity, part_reference, description,
             part_number, product) in values:

            orcad = Orcad()
            orcad.bom = self
            orcad.quantity = quantity.decode(
                encoding='latin1').replace(',', '.')
            orcad.reference = part_reference.decode(encoding='latin1')
            orcad.description = description.decode(encoding='latin1')
            orcad.part_number = part_number.decode(encoding='latin1')
            if product:
                orcad.product, = product

            to_create.append(orcad)
        Orcad.create([x._save_values for x in to_create])

    # Search of the given products exist
    def search_products(self):

        pool = Pool()
        Products = pool.get('product.product')

        def split_lines(lines):
            separated_lines = []
            for line in lines:
                separated_lines.append(line.split('\t'))
            # -1 because the last item is an empty list
            return separated_lines[:-1]

        # Check the number of columns is correct
        ocrad_file = str(self.orcad_file).split('\r\n')
        header = ocrad_file[0].split('\t')

        if len(header) != 4:
            return ([], False)

        lines = ocrad_file[1:]
        items = []
        result = True
        lines = split_lines(lines)

        for (quantity, part_reference, description, part_number) in lines:
            # Check if product exists
            product_exists = Products.search(
                [('code', '=', part_number)])

            items.append((quantity, part_reference,
                description, part_number, product_exists))

            if not product_exists:
                result = False

        return (items, result)

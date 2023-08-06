# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from collections import defaultdict
from trytond.model import (ModelSQL, ModelView, fields,
    sequence_ordered, UnionMixin)
from trytond.pool import Pool
from trytond.pyson import Eval
from sql import Column, Literal
from lxml import etree
from trytond.rpc import RPC
from trytond.transaction import Transaction


class ModelViewMixin:

    @classmethod
    def fields_view_get(cls, view_id=None, view_type='form'):
        view_id = view_id or None
        ViewConfigurator = Pool().get('view.configurator')
        user = Transaction().user or None
        viewConfigurator = ViewConfigurator.search([
            ('model.model','=', cls.__name__),
            ('view','=', view_id),
            ('user', 'in', (None, user))
            ], order=[('user', 'ASC')], limit=1)
        context = Transaction().context
        if (not viewConfigurator or context.get('avoid_custom_view') or
                cls.__name__  == 'view.configurator'):
            result = super(ModelViewMixin, cls).fields_view_get(view_id,
                view_type)
            return result

        view_configurator, = viewConfigurator
        key = (cls.__name__, view_configurator.id)
        result = cls._fields_view_get_cache.get(key)
        if result:
            return result

        result = super(ModelViewMixin, cls).fields_view_get(view_id, view_type)
        if result.get('type') != 'tree':
            return result
        xml = view_configurator.generate_xml()
        parser = etree.XMLParser(remove_blank_text=True)
        tree = etree.fromstring(xml, parser)
        xarch, xfields = cls._view_look_dom_arch(tree, 'tree',
            result['field_childs'])
        result['arch'] = xarch
        result['fields'] = xfields
        cls._fields_view_get_cache.set(key, result)
        return result


class ViewConfiguratorSnapshot(ModelSQL, ModelView):
    'View configurator Snapshot'
    __name__ = 'view.configurator.snapshot'

    view = fields.Many2One('view.configurator', 'View', required=True)
    field = fields.Many2One('ir.model.field', 'Field')
    button = fields.Many2One('ir.model.button', 'Button')


class ViewConfigurator(ModelSQL, ModelView):
    '''View Configurator'''
    __name__ = 'view.configurator'

    model = fields.Many2One('ir.model', 'Model', required=True, select=True)
    model_name = fields.Function(fields.Char('Model Name'),
        'on_change_with_model_name')
    user = fields.Many2One('res.user', 'User')
    view = fields.Many2One('ir.ui.view', 'View', select=True,
        domain=[
        ('type', 'in', (None,'tree')),
        ('model', '=', Eval('model_name')),
        ],
        depends=['model_name'])
    snapshot = fields.One2Many('view.configurator.snapshot', 'view', 'Snapshot',
        readonly=True)
    field_lines = fields.One2Many('view.configurator.line.field', 'view',
        'Lines')
    button_lines = fields.One2Many('view.configurator.line.button', 'view',
        'Lines')
    lines = fields.One2Many('view.configurator.line', 'view',
        'Lines')

    @classmethod
    def __setup__(cls):
        super(ViewConfigurator, cls).__setup__()
        cls._buttons.update({
            'do_snapshot': {},
            })

        cls.__rpc__.update({
            'get_custom_view': RPC(readonly=False, unique=False),
            })

    @classmethod
    def delete(cls, views):
        pool = Pool()
        Snapshot = pool.get('view.configurator.snapshot')
        Lines = pool.get('view.configurator.line')
        snapshots = []
        lines = []
        for view in views:
            snapshots += [x for x in view.snapshot]
            lines += [x for x in view.lines]
        Lines.delete(lines)
        Snapshot.delete(snapshots)
        super(ViewConfigurator, cls).delete(views)

    @classmethod
    def copy(cls, lines, default=None):
        if default is None:
            default = {}
        else:
            default = default.copy()
        default.setdefault('snapshot', None)
        return super(ViewConfigurator, cls).copy(lines, default=default)


    @classmethod
    def get_custom_view(cls, model_name, view_id):
        pool = Pool()
        Model = pool.get('ir.model')
        View = pool.get('ir.ui.view')

        if view_id == 'null':
            view_id = None

        if view_id and view_id != None:
            view_id = int(view_id)

        user = Transaction().user
        domain = [('model.model','=', model_name), ('user', '=', user)]
        if view_id:
            domain += [('view', '=', view_id)]

        custom_views = cls.search(domain, limit=1)
        if custom_views:
            custom_view, = custom_views
            return custom_view.id

        model, = Model.search([('model', '=', model_name)])
        custom_view = cls()
        custom_view.model = model
        if view_id:
            custom_view.view = View(view_id)
        custom_view.user = user
        custom_view.save()
        return custom_view.id

    @fields.depends('model')
    def on_change_with_model_name(self, name=None):
        return self.model and self.model.model or None

    @classmethod
    def create(cls, vlist):
        views = super(ViewConfigurator, cls).create(vlist)
        for view in views:
            view.create_snapshot()
        ModelView._fields_view_get_cache.clear()
        return views

    @classmethod
    def write(cls, views, values, *args):
        super(ViewConfigurator, cls).write(views, values, *args)
        ModelView._fields_view_get_cache.clear()

    def generate_xml(self):
        xml = '<?xml version="1.0"?>\n'
        xml += '<tree>\n'
        new_lines, _ = self.get_difference()

        for line in self.lines + tuple(new_lines):
            if line.field:
                if line.field.ttype == 'datetime':
                    xml+= "<field name='%s' %s %s widget='date'/>\n" % (
                        line.field.name,
                        "expand='"+str(line.expand)+"'" if line.expand else '',
                        "tree_invisible='1'" if line.searchable else '',
                        )
                    xml+= "<field name='%s' %s %s widget='time'/>\n" % (
                        line.field.name,
                        "expand='"+str(line.expand)+"'" if line.expand else '',
                        "tree_invisible='1'" if line.searchable else '',
                        )
                else:
                    xml+= "<field name='%s' %s %s/>\n" % (
                        line.field.name,
                        "expand='"+str(line.expand)+"'" if line.expand else '',
                        "tree_invisible='1'" if line.searchable else '',
                        )
            elif line.button:
                pass
                # TODO: remove on 5.4 and greater
                #xml += "<button name='%s' help='' confirm='' expand='1'/>\n" % (
                #    line.button.name
                #    )
        xml += '</tree>'
        return xml

    def get_difference(self):
        pool = Pool()
        Model = pool.get(self.model.model)
        Snapshot = pool.get('view.configurator.snapshot')
        FieldLine = pool.get('view.configurator.line.field')
        ButtonLine = pool.get('view.configurator.line.button')
        Button = pool.get('ir.model.button')
        with Transaction().set_context(avoid_custom_view=True):
            result = Model.fields_view_get(self.view, view_type='tree')
        parser = etree.XMLParser(remove_comments=True)
        tree = etree.fromstring(result['arch'], parser=parser)

        resources = {}
        existing_snapshot = []
        for field in self.model.fields:
            resources[field.name] = field
        for line in self.snapshot:
            if line.field:
                existing_snapshot.append(line.field)
            elif line.button:
                existing_snapshot.append(line.button)

        sbuttons = Button.search([('model', '=', self.model)])
        for button in sbuttons:
            resources[button.name] = button

        def create_lines(type_, resource, expand, invisible):
            if type_ == 'field':
                line = FieldLine()
                line.type = 'ir.model.field'
                line.field = resource
                line.view = self
                line.sequence=100
            elif type_ == 'button':
                line = ButtonLine()
                line.type = 'ir.model.button'
                line.button = resource
                line.view = self
                line.sequence=900
            line.searchable = invisible
            line.expand=expand
            return line

        def create_snapshot(type_, resource, expand, invisible):
            snapshot = Snapshot()
            snapshot.view = self
            if type_ == 'field':
                snapshot.field = resource
            else:
                snapshot.button = resource
            snapshot.invisible = invisible
            snapshot.expand = expand
            snapshot.view = self
            existing_snapshot.append(resource)
            return snapshot

        lines = []
        snapshots = []
        for child in tree:
            type_ = child.tag
            attributes = child.attrib
            name = attributes['name']
            expand = attributes.get('expand', None)
            invisible = attributes.get('tree_invisible', False)
            if resources[name] not in existing_snapshot:
                line = create_lines(type_, resources[name], expand, invisible)
                snap = create_snapshot(type_, resources[name], expand, invisible)
                if line:
                    lines.append(line)
                if snap:
                    snapshots.append(snap)
        return lines, snapshots

    def create_snapshot(self):
        pool = Pool()
        Snapshot = pool.get('view.configurator.snapshot')
        FieldLine = pool.get('view.configurator.line.field')

        (lines, snapshots) = self.get_difference()
        FieldLine.save(lines)
        Snapshot.save(snapshots)


    @classmethod
    @ModelView.button
    def do_snapshot(cls, views):
        for view in views:
            view.create_snapshot()


class ViewConfiguratorLineButton(sequence_ordered(), ModelSQL, ModelView):
    '''View Configurator Line Button'''
    __name__ = 'view.configurator.line.button'

    view = fields.Many2One('view.configurator',
        'View Configurator', required=True)
    button = fields.Many2One('ir.model.button', 'Button',
        domain=[
            ('model', '=', Eval('parent_model')),
        ], depends=['parent_model'])
    expand = fields.Integer('Expand')
    searchable = fields.Boolean('Searchable')
    type = fields.Selection([
        ('ir.model.button', 'Button'),
        ], 'Type')
    parent_model = fields.Function(fields.Many2One('ir.model', 'Model'),
        'on_change_with_parent_model')

    @staticmethod
    def default_type():
        return 'ir.model.button'

    @fields.depends('view', '_parent_view.model')
    def on_change_with_parent_model(self, name=None):
        return self.view.model.id if self.view else None


class ViewConfiguratorLineField(sequence_ordered(),ModelSQL, ModelView):
    '''View Configurator Line Field'''
    __name__ = 'view.configurator.line.field'

    view = fields.Many2One('view.configurator',
        'View Configurator', required=True)
    field = fields.Many2One('ir.model.field', 'Field',
        domain=[
            ('model', '=', Eval('parent_model')),
        ], depends=['parent_model'])
    expand = fields.Integer('Expand')
    searchable = fields.Boolean('Searchable')
    type = fields.Selection([
        ('ir.model.field', 'Field'),
        ], 'Type')
    parent_model = fields.Function(fields.Many2One('ir.model', 'Model'),
        'on_change_with_parent_model')

    @staticmethod
    def default_type():
        return 'ir.model.field'

    @fields.depends('view', '_parent_view.model')
    def on_change_with_parent_model(self, name=None):
        return self.view.model.id if self.view else None


class ViewConfiguratorLine(UnionMixin, sequence_ordered(), ModelSQL, ModelView):
    '''View Configurator Line'''
    __name__ = 'view.configurator.line'

    view = fields.Many2One('view.configurator',
        'View Configurator', ondelete='CASCADE', required=True)
    type = fields.Selection([
        ('ir.model.button', 'Button'),
        ('ir.model.field', 'Field'),
        ], 'Type', required=True)
    field = fields.Many2One('ir.model.field', 'Field',
        domain=[('model', '=',
            Eval('_parent_view', Eval('context', {})).get('model', -1))
        ], states={
            'required': Eval('type') == 'ir.model.field',
            'invisible': Eval('type') != 'ir.model.field',
        }, depends=['type'])
    button = fields.Many2One('ir.model.button', 'Button',
        domain=[('model', '=',
            Eval('_parent_view', Eval('context', {})).get('model', -1))
        ], states={
            'required': Eval('type') == 'ir.model.button',
            'invisible': Eval('type') != 'ir.model.button',
        }, depends=['type'])
    expand = fields.Integer('Expand',
        states={
        }, depends=['type'])
    searchable = fields.Boolean('Searchable',
        states={
            'invisible': Eval('type') != 'ir.model.field',
        }, depends=[ 'type'])
    parent_model = fields.Function(fields.Many2One('ir.model', 'Model'),
        'on_change_with_parent_model')
    model_name = fields.Function(fields.Char('Model Name'),
        'on_change_with_model_name')

    @staticmethod
    def default_searchable():
        return False

    @staticmethod
    def default_type():
        return 'ir.model.field'

    @fields.depends('view', '_parent_view.model')
    def on_change_with_parent_model(self, name=None):
        return self.view.model.id if self.view else None

    @fields.depends('parent_model')
    def on_change_with_model_name(self, name=None):
        return self.parent_model and self.parent_model.model or None

    @staticmethod
    def union_models():
        return ['view.configurator.line.field',
            'view.configurator.line.button']

    @classmethod
    def union_column(cls, name, field, table, Model):
        value = Literal(None)
        if name == 'button':
            if 'button' in Model.__name__:
                value = Column(table, 'button')
            return value
        if name == 'field':
            if 'field' in Model.__name__:
                value = Column(table, 'field')
            return value
        return super(ViewConfiguratorLine, cls).union_column(name,
            field, table, Model)

    @classmethod
    def create(cls, vlist):
        pool = Pool()

        models_to_create = defaultdict(list)
        for line in vlist:
            type_ = 'view.configurator.line.field'
            if 'button' in line['type'] :
                type_ = 'view.configurator.line.button'
                if 'field' in line:
                    del line['field']
            else:
                if 'button' in line:
                    del line['button']
            models_to_create[type_].append(line)

        for model, arguments in models_to_create.items():
            Model = pool.get(model)
            Model.create(arguments)

    @classmethod
    def write(cls, *args):
        pool = Pool()
        models_to_write = defaultdict(list)
        actions = iter(args)
        for models, values in zip(actions, actions):
            for model in models:
                record = cls.union_unshard(model.id)
                models_to_write[record.__name__].extend(([record], values))
        for model, arguments in models_to_write.items():
            Model = pool.get(model)
            Model.write(*arguments)

    @classmethod
    def delete(cls, lines):
        pool = Pool()
        models_to_delete = defaultdict(list)
        for model in lines:
            record = cls.union_unshard(model.id)
            models_to_delete[record.__name__].append(record)
        for model, records in models_to_delete.items():
            Model = pool.get(model)
            Model.delete(records)

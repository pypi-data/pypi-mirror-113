# encoding: utf-8
# This file is part product_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
import slug
import unicodedata
from simpleeval import simple_eval
from genshi.template import NewTextTemplate as TextTemplate
from jinja2 import Template as Jinja2Template
from trytond.config import config as config_

template_engine = config_.get('product', 'template_engine', default='genshi')

SRC_CHARS = u"""/*+?¿!&$[]{}`^<>=~%|\\"""

def unaccent(text):
    if not text:
        return ''
    for c in range(len(SRC_CHARS)):
        text = text.replace(SRC_CHARS[c], '')
    text = text.replace('º', '. ')
    text = text.replace('ª', '. ')
    text = text.replace('  ', ' ')
    output = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore')
    return output.decode('utf-8')

def slugify(value):
    """Convert value to slug: az09 and replace spaces by -"""
    return slug.slug(value)

def seo_lenght(string):
    '''Get first 155 characters from string'''
    if len(string) > 155:
        return '%s...' % (string[:152])
    return string

def esale_eval(expression, record):
    '''Evaluates the given :attr:expression

    :param expression: Expression to evaluate
    :param record: The browse record of the record
    '''
    if template_engine == 'genshi':
        return _engine_genshi(expression, record)
    elif template_engine == 'jinja2':
        return _engine_jinja2(expression, record)
    else:
        return _engine_python(expression, record)

def template_context(record):
    """ Generate the template context
    This is mainly to assist in the inheritance pattern
    """
    return {'record': record}

def _engine_python(expression, record):
    '''Evaluate the pythonic expression and return its value
    '''
    if expression is None:
        return ''
    tpl_context = template_context(record)
    return simple_eval(expression, tpl_context)

def _engine_genshi(expression, record):
    '''
    :param expression: Expression to evaluate
    :param record: Browse record
    '''
    if not expression:
        return ''
    template = TextTemplate(expression)
    tpl_context = template_context(record)
    return template.generate(**tpl_context).render(encoding='UTF-8')

def _engine_jinja2(expression, record):
    '''
    :param expression: Expression to evaluate
    :param record: Browse record
    '''
    if not expression:
        return ''
    template = Jinja2Template(expression)
    tpl_context = template_context(record)
    return template.render(tpl_context).encode('utf-8')

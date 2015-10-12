# -*- coding: utf-8 -*-
from django import template
from ..models import Style

register = template.Library()

@register.inclusion_tag('templatetags/style.html', takes_context=True)
def add_classes(context):
    styles = Style.objects.all().select_related('plugin')\
        .prefetch_related('styleclasses', 'source_styleclasses')
    context['styles'] = styles
    return context

@register.filter
def lines(value):
    if isinstance(value, list):
        return ','.join([str(x[0]) for x in value])
    elif isinstance(value, tuple):
        return value[0]
    else:
        # TODO: Use regular expression
        if value.startswith('[') and value.endswith(']'):
            tmp = value.strip('[').strip(']').split(',')
            return ','.join(tmp[x].strip().strip('(') for x in range(0, len(tmp), 2))
        else:
            return value.split(',')[0].strip('(')

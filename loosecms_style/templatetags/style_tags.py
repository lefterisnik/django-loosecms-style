# -*- coding: utf-8 -*-
from django import template
from ..models import Style

register = template.Library()

@register.inclusion_tag('templatetags/style.html', takes_context=True)
def add_classes(context):
    styles = Style.objects.all()
    context['styles'] = styles
    return context
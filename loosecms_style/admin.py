# -*- coding: utf-8 -*-
from django import forms
from django.db import models
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Style, StyleClass, StyleClassAttribute


class StyleAdmin(admin.ModelAdmin):
    filter_horizontal = ('styleclasses',)
    readonly_fields = ('source_styleclasses',)


class StyleClassAttributeInline(admin.StackedInline):
    model = StyleClassAttribute
    extra = 1
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 5})},
    }


class StyleClassAdmin(admin.ModelAdmin):
    inlines = [
        StyleClassAttributeInline
    ]
    search_fields = ['title']
    list_filter = ('styleclassattribute__override', )
    formfield_overrides = {
        models.TextField: {'widget': forms.Textarea(attrs={'rows': 5})},
    }

admin.site.register(Style, StyleAdmin)
admin.site.register(StyleClass, StyleClassAdmin)
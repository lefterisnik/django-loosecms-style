# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Style, StyleClass, StyleClassAttribute


class StyleAdmin(admin.ModelAdmin):
    filter_horizontal = ('styleclasses',)
    readonly_fields = ('source_styleclasses',)


class StyleClassAttributeInline(admin.StackedInline):
    model = StyleClassAttribute
    extra = 1


class StyleClassAdmin(admin.ModelAdmin):
    inlines = [
        StyleClassAttributeInline
    ]

admin.site.register(Style, StyleAdmin)
admin.site.register(StyleClass, StyleClassAdmin)
# -*- coding: utf-8 -*-
import os
from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _

from loosecms.models import Plugin

from .signals import update_css_file


class StyleClass(models.Model):
    title = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('class')
        verbose_name_plural = _('classes')


class StyleClassAttribute(models.Model):
    title = models.TextField()
    css = models.TextField()
    styleclass = models.ForeignKey(StyleClass)
    override = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('class attribute')
        verbose_name_plural = _('class attributes')


class Style(models.Model):
    title = models.CharField(max_length=50, unique=True)
    plugin = models.ForeignKey(Plugin)
    original_html = models.TextField(default='')
    html_tag = models.CharField(max_length=50)
    html_id = models.CharField(max_length=50, unique=True, blank=True)
    source_styleclasses = models.ManyToManyField(StyleClass, related_name='source_styleclasses')
    styleclasses = models.ManyToManyField(StyleClass)
    source_css = models.TextField(blank=True)
    css = models.TextField(blank=True)
    description = models.TextField(blank=True)
    element_is_grid = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

post_save.connect(update_css_file, sender=StyleClassAttribute)

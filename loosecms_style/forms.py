# -*- coding:utf-8 -*-
from django import forms
from django.forms.formsets import BaseFormSet
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper, FilteredSelectMultiple

from .models import *


class BaseStyleFormSet(BaseFormSet):

    def __init__(self, admin_site, *args, **kwargs):
        self.admin_site = admin_site
        super(BaseStyleFormSet, self).__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        defaults = {
            'admin_site': self.admin_site,
        }
        defaults.update(kwargs)
        return super(BaseStyleFormSet, self)._construct_form(i, **defaults)


class StyleForm(forms.Form):
    required_css_class = 'required'

    title = forms.CharField(max_length=150)

    original_html = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}),
                                    max_length=150)
    html_tag = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}),
                               max_length=150,
                               required=True)
    html_id = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}),
                              max_length=150,
                              required=False)
    source_css = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'readonly': True}),
                                 required=False)
    css = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}),
                          required=False)
    source_styleclasses = forms.CharField(required=False,
                                          widget=forms.TextInput(attrs={'readonly': True}))

    styleclasses = forms.ModelMultipleChoiceField(queryset=StyleClass.objects.all(),
                                                  required=False)
    position = forms.CharField(widget=forms.HiddenInput(),
                               max_length=100,
                               required=False)

    def __init__(self, *args, **kwargs):
        self.admin_site = kwargs.pop('admin_site', None)
        super(StyleForm, self).__init__(*args, **kwargs)
        self.fields['styleclasses'].widget = RelatedFieldWidgetWrapper(FilteredSelectMultiple('Classes', True),
                                                                       Style._meta.get_field('styleclasses').rel,
                                                                       self.admin_site, can_change_related=True)
        self.fields['styleclasses'].queryset = StyleClass.objects.all()
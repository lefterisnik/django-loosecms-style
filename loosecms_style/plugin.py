# -*- coding: utf-8 -*-
import re
from bs4 import BeautifulSoup

from django.apps import apps
from django.conf import settings
from django.conf.urls import url
from django.template import loader
from django.shortcuts import render
from django.core.cache import cache
from django.core import urlresolvers
from django.template import RequestContext
from django.contrib.staticfiles import finders
from django.shortcuts import get_object_or_404
from django.forms.formsets import formset_factory
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, JsonResponse, Http404


from .utils import *
from .forms import *
from .models import *

from loosecms.models import Plugin, HtmlPage
from loosecms.plugin_pool import plugin_pool
from loosecms.plugin_modeladmin import PluginModelAdmin


class StylePlugin(PluginModelAdmin):
    model = Style
    name = _('Style')
    plugin_extra_links = True
    template_link = "plugin/loosecms/style_link.html"

    def render_link(self, context, plugin):
        exclude_style_plugins = getattr(settings, 'EXCLUDE_STYLE_PLUGINS', None)

        if exclude_style_plugins and plugin.type not in exclude_style_plugins:
            template = loader.get_template(self.template_link)
            context['app'] = apps.get_app_config('loosecms_style').verbose_name
            context['plugin'] = plugin
            return template.render(context)
        else:

            return ''

    def get_urls(self):
        """
        Add custom urls to page admin.
        :return: urls
        """
        style_urls = [
            url(r'^edit_style/(?P<pk>\d+)/$', self.admin_site.admin_view(self.edit_style),
                name='admin_edit_style'),
        ]

        return style_urls

    def edit_style(self, request, pk):
        """
        Prompt edit style form for requested plugin
        :param request:
        :param pk:
        :return: HTML (edit_style_form) or a script that close popup window
        """
        plugin = get_object_or_404(Plugin, pk=pk)

        # Create the modeladmin instance of the plugin
        plugin_modeladmin_cls = plugin_pool.plugins[plugin.type]
        plugin_model = plugin_modeladmin_cls.model
        plugin_modeladmin = plugin_modeladmin_cls(plugin_model, self.admin_site)

        # Fetch the plugin manager that contain the appropriate context variables
        plugin_manager = get_object_or_404(plugin_model, pk=pk)

        if plugin_modeladmin.__class__.__name__ == 'RowPlugin':
            rendered_template = '<div class="row" id="cms_plugin_' + str(plugin_manager.pk) + '">'
        elif plugin_modeladmin.__class__.__name__ == 'ColumnPlugin':
            rendered_template = '<div class="col-lg-' + str(plugin_manager.width) + '" id="cms_plugin_' + str(plugin_manager.pk) + '">'
        else:
            if plugin_modeladmin.template:
                # TODO: Find a way to render plugin template as will showed properly in the page
                request_context = RequestContext(request)
                rendered_template = plugin_modeladmin.render_to_string(request_context, plugin_manager)

        # Normalize template without whitespaces
        lines = rendered_template.split('\n')
        rendered_template = '\n'.join([line for line in lines if not re.match(r'^\s*$', line)])

        if request.method == 'GET':
            # Find all html tags from the template
            # Exam if it is in cache else set it to the cache with timeout 15 * 60 = 15 minutes
            parser = cache.get(plugin.pk)
            if not parser:
                parser = MyHtmlParser()
                parser.feed(rendered_template)
                cache.set(plugin.pk, parser, 60*15)

                # Find all css of the project and pass it to the css list
                csss = []
                for finder in finders.get_finders():
                    for file_ in list(finder.list(['*.js', '*.min.css', '*.woff2', '*.svg', '*.eot', '*.woff', '*.ttf',
                                                  '*.png', '*.jpg', '*.otf', '*.psd', '*.map', '*.txt', '*.gif',
                                                  '*.md', '*admin*', '*ckeditor*', '*loosecms_style*'])):
                        csss.append(finders.find(file_[0]))

                # Call utils function which finds all css attributes given template
                populate_cssclasses_attrs(csss, parser.plugin_style)

            StyleFormSet = formset_factory(StyleForm, formset=BaseStyleFormSet, extra=0, can_delete=True)
            formset = StyleFormSet(initial=get_initial_values(parser.plugin_style, plugin), admin_site=self.admin_site)

            context = dict(
                # Include common variables for rendering the admin template.
                self.admin_site.each_context(request),
                current_app=self.admin_site.name,
                title=_('Edit stylesheet'),
                formset=formset,
                media = self.media + formset.media,
                is_popup=True,
                template=rendered_template,
                form_url=urlresolvers.reverse('admin:admin_edit_style', args=(pk,))
            )
            return render(request, 'admin/edit_style_form.html', context)

        if request.method == 'POST':
            StyleFormSet = formset_factory(StyleForm, formset=BaseStyleFormSet, can_delete=True)
            formset = StyleFormSet(data=request.POST, files=request.FILES, admin_site=self.admin_site)

            if formset.is_valid():
                for form in formset:
                    pk = form.cleaned_data['pk']
                    title = form.cleaned_data['title']
                    original_html = form.cleaned_data['original_html']
                    html_tag = form.cleaned_data['html_tag']
                    html_id = form.cleaned_data['html_id']
                    source_css = form.cleaned_data['source_css']
                    css = form.cleaned_data['css']
                    styleclasses = form.cleaned_data['styleclasses']
                    source_styleclasses = form.cleaned_data['source_styleclasses']

                    if form in formset.deleted_forms:
                        try:
                            style = Style.objects.get(pk=pk)
                            style.delete()
                            continue
                        except Style.DoesNotExist:
                            pass

                    source_styleclasses = [x for x in source_styleclasses.split(',')]
                    source_styleclasses_queryset = StyleClass.objects.filter(title__in=source_styleclasses)

                    update_values = dict(
                        title=title,
                        plugin=plugin,
                        original_html=original_html,
                        html_tag=html_tag,
                        html_id=html_id,
                        source_css=source_css,
                        css=css
                    )

                    if plugin.type == 'RowPlugin' or plugin.type == 'ColumnPlugin':
                        update_values.update(
                            element_is_grid=True
                        )
                    else:
                        update_values.update(
                            element_is_grid=False
                        )

                    style, created = Style.objects.update_or_create(pk=pk, defaults=update_values)

                    style.styleclasses.clear()
                    style.source_styleclasses.clear()
                    for styleclass in styleclasses:
                        if styleclass in source_styleclasses_queryset:
                            form.add_error('styleclasses', '%s styleclass is arleady in source styleclasess' % styleclass)
                            context = dict(
                                # Include common variables for rendering the admin template.
                                self.admin_site.each_context(request),
                                current_app=self.admin_site.name,
                                title=_('Edit stylesheet'),
                                formset=formset,
                                media = self.media + formset.media,
                                is_popup=True,
                                template=rendered_template,
                                form_url=urlresolvers.reverse('admin:admin_edit_style', args=(pk,))
                            )
                            return render(request, 'admin/edit_style_form.html', context)
                        style.styleclasses.add(styleclass)

                    for source_styleclass in source_styleclasses_queryset:
                        style.source_styleclasses.add(source_styleclass)

                return HttpResponse('<script>window.parent.location.reload(true);self.close();</script>')
            else:
                context = dict(
                    # Include common variables for rendering the admin template.
                    self.admin_site.each_context(request),
                    current_app=self.admin_site.name,
                    title=_('Edit stylesheet'),
                    formset=formset,
                    media = self.media + formset.media,
                    is_popup=True,
                    template=rendered_template,
                    form_url=urlresolvers.reverse('admin:admin_edit_style', args=(pk,))
                )
                return render(request, 'admin/edit_style_form.html', context)

plugin_pool.register_plugin(StylePlugin)
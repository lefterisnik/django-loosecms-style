# -*- coding: utf-8 -*-
from django.core import files
from django.conf import settings
from django.contrib.staticfiles import finders


def update_css_file(sender, instance, created, **kwargs):
    # TODO: Not efficient as it fetches for each change or add all objects and rewrite hole file
    # Case 1: Maybe user edit file manually so changes will be lost
    # Case 2: If multiple add or changes occurs will be executed to many queries
    styleclassattrs = sender.objects.filter(override=True)
    if settings.DEBUG:
        result = finders.find('loosecms_style/css/style.css')
    else:
        result = settings.STATIC_ROOT + '/loosecms_style/css/style.css'
    with open(result, 'w') as file_:
        style_css = files.File(file_)

        for styleclassattr in styleclassattrs:
            style_css.write('%s {\n' % styleclassattr.title)
            style_css.write(styleclassattr.css)
            style_css.write('}\n')

        style_css.close()
        file_.close()


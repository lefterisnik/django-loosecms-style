# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0005_style_original_html'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='source_css',
            field=models.TextField(blank=True),
        ),
    ]

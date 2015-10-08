# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0004_style_source_styleclasses'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='original_html',
            field=models.TextField(default=b''),
        ),
    ]

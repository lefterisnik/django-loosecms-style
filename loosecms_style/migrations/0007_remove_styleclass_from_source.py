# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0006_style_source_css'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='styleclass',
            name='from_source',
        ),
    ]

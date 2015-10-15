# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0009_auto_20151012_1229'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='style',
            options={'verbose_name': 'style', 'verbose_name_plural': 'styles'},
        ),
    ]

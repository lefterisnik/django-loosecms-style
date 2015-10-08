# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='styleclass',
            options={'verbose_name': 'class', 'verbose_name_plural': 'classes'},
        ),
        migrations.AlterModelOptions(
            name='styleclassinherit',
            options={'verbose_name': 'class attribute', 'verbose_name_plural': 'class attributes'},
        ),
    ]

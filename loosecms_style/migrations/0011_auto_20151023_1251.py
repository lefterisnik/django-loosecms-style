# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0010_auto_20151013_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='html_id',
            field=models.CharField(max_length=50, unique=True, null=True, blank=True),
        ),
    ]

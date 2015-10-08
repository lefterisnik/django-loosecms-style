# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0007_remove_styleclass_from_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='styleclass',
            name='override',
        ),
        migrations.AddField(
            model_name='styleclassattribute',
            name='override',
            field=models.BooleanField(default=False),
        ),
    ]

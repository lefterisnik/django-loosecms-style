# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0003_auto_20151008_1009'),
    ]

    operations = [
        migrations.AddField(
            model_name='style',
            name='source_styleclasses',
            field=models.ManyToManyField(related_name='source_styleclasses', to='loosecms_style.StyleClass'),
        ),
    ]

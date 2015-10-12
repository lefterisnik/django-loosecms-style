# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0008_auto_20151008_2055'),
    ]

    operations = [
        migrations.AlterField(
            model_name='style',
            name='source_styleclasses',
            field=models.ManyToManyField(related_name='source_styleclasses', to='loosecms_style.StyleClass', blank=True),
        ),
        migrations.AlterField(
            model_name='style',
            name='styleclasses',
            field=models.ManyToManyField(to='loosecms_style.StyleClass', blank=True),
        ),
    ]

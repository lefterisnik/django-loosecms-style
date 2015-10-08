# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms_style', '0002_auto_20151008_0956'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StyleClassInherit',
            new_name='StyleClassAttribute',
        ),
    ]

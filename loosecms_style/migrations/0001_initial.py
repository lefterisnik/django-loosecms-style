# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('loosecms', '0010_auto_20151006_2056'),
    ]

    operations = [
        migrations.CreateModel(
            name='Style',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=50)),
                ('html_tag', models.CharField(max_length=50)),
                ('html_id', models.CharField(unique=True, max_length=50, blank=True)),
                ('css', models.TextField(blank=True)),
                ('description', models.TextField(blank=True)),
                ('element_is_grid', models.BooleanField(default=False)),
                ('plugin', models.ForeignKey(to='loosecms.Plugin')),
            ],
        ),
        migrations.CreateModel(
            name='StyleClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(null=True, blank=True)),
                ('from_source', models.BooleanField(default=False)),
                ('override', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'classes',
                'verbose_name_plural': 'classes',
            },
        ),
        migrations.CreateModel(
            name='StyleClassInherit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.TextField()),
                ('css', models.TextField()),
                ('styleclass', models.ForeignKey(to='loosecms_style.StyleClass')),
            ],
            options={
                'verbose_name': 'classes inheritance',
                'verbose_name_plural': 'classes inheritance',
            },
        ),
        migrations.AddField(
            model_name='style',
            name='styleclasses',
            field=models.ManyToManyField(to='loosecms_style.StyleClass'),
        ),
    ]

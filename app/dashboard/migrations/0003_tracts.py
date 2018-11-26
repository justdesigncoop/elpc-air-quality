# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-21 21:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0002_auto_20180312_0316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tracts',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('display', models.CharField(blank=True, max_length=40, null=True)),
                ('geo', models.TextField(blank=True, null=True)),
            ],
            options={
                'db_table': 'tracts',
                'managed': False,
                'verbose_name_plural': 'tracts',
            },
        ),
    ]
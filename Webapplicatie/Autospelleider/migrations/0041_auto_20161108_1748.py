# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 17:48
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Autospelleider', '0040_auto_20161108_1731'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 17, 48, 53, 456738)),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 20:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Autospelleider', '0044_auto_20161108_2015'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='reservation_ID',
            field=models.IntegerField(blank=True, default=-1, null=True),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 20, 51, 4, 830977)),
        ),
    ]

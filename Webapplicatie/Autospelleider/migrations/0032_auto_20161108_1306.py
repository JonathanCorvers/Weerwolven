# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 13:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Autospelleider', '0031_auto_20161026_0241'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservation',
            name='completed',
        ),
        migrations.RemoveField(
            model_name='reservation',
            name='reservation_ID',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='amount_paid',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 8, 13, 6, 36, 400994)),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='voorverkoop',
            field=models.BooleanField(default=True),
        ),
    ]
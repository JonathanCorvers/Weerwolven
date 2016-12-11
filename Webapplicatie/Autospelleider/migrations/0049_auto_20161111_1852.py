# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 18:52
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Autospelleider', '0048_auto_20161111_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 11, 18, 52, 37, 780976)),
        ),
        migrations.AlterField(
            model_name='reservationsubscription',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 11, 18, 52, 37, 816978)),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Autospelleider.GroupSubscription'),
        ),
        migrations.AlterField(
            model_name='subscription',
            name='reservation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Autospelleider.ReservationSubscription'),
        ),
    ]

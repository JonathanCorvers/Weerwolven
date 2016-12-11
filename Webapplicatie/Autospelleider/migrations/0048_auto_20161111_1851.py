# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-11 18:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Autospelleider', '0047_auto_20161111_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReservationSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_ID', models.IntegerField(blank=True, default=-1, null=True)),
                ('amount_paid', models.PositiveIntegerField(default=0)),
                ('voorverkoop', models.BooleanField(default=True)),
                ('creation_time', models.DateTimeField(default=datetime.datetime(2016, 11, 11, 18, 51, 3, 566587))),
            ],
        ),
        migrations.AlterField(
            model_name='reservation',
            name='creation_time',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 11, 18, 51, 3, 532585)),
        ),
    ]

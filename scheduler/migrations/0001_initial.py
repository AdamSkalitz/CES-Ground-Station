# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 23:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SatelliteName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=70, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TLE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('line1', models.CharField(max_length=70)),
                ('line2', models.CharField(max_length=70)),
                ('satellitename', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='scheduler.SatelliteName')),
            ],
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-11 01:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TLE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='NAME', max_length=30, unique=True)),
                ('line1', models.CharField(max_length=70)),
                ('line2', models.CharField(max_length=70)),
            ],
            options={
                'ordering': ('name',),
            },
        ),
    ]

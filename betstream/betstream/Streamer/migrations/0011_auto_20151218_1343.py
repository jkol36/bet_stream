# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-18 18:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Streamer', '0010_auto_20151216_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='is_win',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='bet',
            name='stake',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
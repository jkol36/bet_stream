# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-15 15:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Streamer', '0004_bovadabet_match_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='edgebet',
            name='is_placed',
        ),
        migrations.AddField(
            model_name='bet',
            name='is_placed',
            field=models.BooleanField(default=False),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-16 16:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Streamer', '0007_lastfetch'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Lastfetch',
            new_name='fetches',
        ),
    ]

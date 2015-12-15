# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-14 15:53
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Streamer', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='edgebet',
            name='is_placed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='edgebet',
            name='recieved',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='edgebet',
            name='sibling',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='Streamer.Bovadabet'),
        ),
    ]

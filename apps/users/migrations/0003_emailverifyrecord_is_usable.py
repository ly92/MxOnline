# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-13 13:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20170831_2230'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailverifyrecord',
            name='is_usable',
            field=models.BooleanField(default=True),
        ),
    ]
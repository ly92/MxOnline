# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-25 16:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20170915_1002'),
        ('courses', '0003_auto_20170915_1418'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='teacher',
            field=models.ForeignKey(default=59, on_delete=django.db.models.deletion.CASCADE, to='organization.Teacher', verbose_name='所属讲师'),
            preserve_default=False,
        ),
    ]

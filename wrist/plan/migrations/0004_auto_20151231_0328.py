# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-31 03:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0003_tag_matchs'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='matchs',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='plans',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
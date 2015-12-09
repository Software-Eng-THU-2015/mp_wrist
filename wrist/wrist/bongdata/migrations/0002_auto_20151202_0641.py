# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bongdata', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bongdata',
            name='user',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='bongdata',
            name='userId',
            field=models.CharField(default=0, max_length=30),
            preserve_default=False,
        ),
    ]

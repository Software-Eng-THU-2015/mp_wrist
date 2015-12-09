# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bongdata', '0002_auto_20151202_0641'),
    ]

    operations = [
        migrations.AddField(
            model_name='bongdata',
            name='date',
            field=models.IntegerField(default=0),
        ),
    ]

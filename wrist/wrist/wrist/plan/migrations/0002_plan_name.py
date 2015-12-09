# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='name',
            field=models.CharField(default='test', max_length=30),
            preserve_default=False,
        ),
    ]

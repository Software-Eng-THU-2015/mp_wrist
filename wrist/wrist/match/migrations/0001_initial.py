# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0004_auto_20151202_0641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=100)),
                ('description', models.TextField(default=b'')),
                ('goal', models.IntegerField(default=0)),
                ('goods', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(related_name='user_match', to='basic.User')),
                ('members', models.ManyToManyField(related_name='team_match', to='basic.Team')),
            ],
        ),
    ]

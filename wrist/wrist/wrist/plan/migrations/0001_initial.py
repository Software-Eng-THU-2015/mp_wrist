# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('starttime', models.CharField(max_length=30)),
                ('endtime', models.CharField(max_length=30)),
                ('goal_0', models.IntegerField()),
                ('goal_1', models.IntegerField()),
                ('goal_2', models.IntegerField()),
                ('goods', models.IntegerField()),
                ('members', models.ManyToManyField(related_name='members_plan', to='basic.User')),
                ('owner', models.ForeignKey(related_name='owner_plan', to='basic.User')),
            ],
        ),
    ]

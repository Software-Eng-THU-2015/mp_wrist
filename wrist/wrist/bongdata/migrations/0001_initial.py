# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BongData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startTime', models.CharField(max_length=30)),
                ('endTime', models.CharField(max_length=30)),
                ('type', models.IntegerField(default=0)),
                ('subType', models.IntegerField(default=0)),
                ('distance', models.IntegerField(default=0)),
                ('speed', models.IntegerField(default=0)),
                ('calories', models.IntegerField(default=0)),
                ('steps', models.IntegerField(default=0)),
                ('actTime', models.IntegerField(default=0)),
                ('nonActTime', models.IntegerField(default=0)),
                ('dsNum', models.IntegerField(default=0)),
                ('lsNum', models.IntegerField(default=0)),
                ('wakeNum', models.IntegerField(default=0)),
                ('wakeTimes', models.IntegerField(default=0)),
                ('score', models.IntegerField(default=0)),
            ],
        ),
    ]

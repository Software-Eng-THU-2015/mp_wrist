# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
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
        migrations.AddField(
            model_name='team',
            name='goods',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='goods',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='data',
            name='user',
            field=models.ForeignKey(related_name='basic_data', to='basic.User'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0003_auto_20151111_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='DayDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.IntegerField()),
                ('steps', models.IntegerField(default=0)),
                ('calories', models.IntegerField(default=0)),
                ('sleep', models.IntegerField(default=0)),
                ('distance', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='data',
            name='date',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='uid',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='data',
            name='user',
            field=models.ForeignKey(related_name='user_data', to='basic.User'),
        ),
        migrations.AlterField(
            model_name='team',
            name='goods',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='user_team', to='basic.User'),
        ),
        migrations.AlterField(
            model_name='user',
            name='goods',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='daydate',
            name='user',
            field=models.ForeignKey(related_name='user_daydata', to='basic.User'),
        ),
        migrations.AddField(
            model_name='archive',
            name='owners',
            field=models.ManyToManyField(related_name='user_archive', to='basic.User'),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 21:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Archive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField(default=0)),
                ('bongdata_id', models.IntegerField(default=0)),
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
        migrations.CreateModel(
            name='DayData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.IntegerField()),
                ('steps', models.IntegerField(default=0)),
                ('calories', models.IntegerField(default=0)),
                ('distance', models.IntegerField(default=0)),
                ('sleep', models.IntegerField(default=0)),
                ('steps_goal', models.IntegerField(default=0)),
                ('calories_goal', models.IntegerField(default=0)),
                ('distance_goal', models.IntegerField(default=0)),
                ('sleep_goal', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Good',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('target', models.IntegerField(default=0)),
                ('type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('type', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.CharField(default=b'', max_length=200)),
                ('sex', models.IntegerField(default=0)),
                ('height', models.IntegerField(default=0)),
                ('weight', models.IntegerField(default=0)),
                ('openId', models.CharField(max_length=150)),
                ('goods', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('uid', models.CharField(default=b'', max_length=100)),
                ('dayPlan', models.IntegerField(default=0)),
                ('sleepPlan', models.IntegerField(default=0)),
                ('comment', models.TextField(blank=True, default=b'')),
                ('friends', models.ManyToManyField(blank=True, related_name='_user_friends_+', to='basic.User')),
            ],
        ),
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(related_name='user_team_members', to='basic.User'),
        ),
        migrations.AddField(
            model_name='good',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_good_user', to='basic.User'),
        ),
        migrations.AddField(
            model_name='daydata',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_daydata_user', to='basic.User'),
        ),
        migrations.AddField(
            model_name='data',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_data_user', to='basic.User'),
        ),
        migrations.AddField(
            model_name='archive',
            name='owners',
            field=models.ManyToManyField(related_name='user_archive_owners', to='basic.User'),
        ),
    ]

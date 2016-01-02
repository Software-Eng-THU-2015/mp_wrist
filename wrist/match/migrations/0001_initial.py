# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-23 18:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('basic', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=b'', max_length=100)),
                ('description', models.TextField(default=b'')),
                ('startTime', models.CharField(default=b'', max_length=20)),
                ('endTime', models.CharField(default=b'', max_length=20)),
                ('endDate', models.IntegerField(default=0)),
                ('endDateTime', models.IntegerField(default=0)),
                ('image', models.CharField(default=b'', max_length=200)),
                ('finished', models.IntegerField(default=0)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_match_creator', to='basic.User')),
                ('members', models.ManyToManyField(related_name='team_match_members', to='basic.Team')),
            ],
        ),
    ]

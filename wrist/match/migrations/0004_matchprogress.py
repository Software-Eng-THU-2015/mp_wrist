# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-05 02:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0001_initial'),
        ('match', '0003_match_user_members'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchProgress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='match_matchprogress_match', to='match.Match')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_matchprogress_user', to='basic.User')),
            ],
        ),
    ]

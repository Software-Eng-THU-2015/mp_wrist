# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plan', '0002_plan_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='plan',
            name='createTime',
            field=models.CharField(default='20151111', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plan',
            name='description',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='plan',
            name='images',
            field=models.TextField(default=b''),
        ),
        migrations.AlterField(
            model_name='plan',
            name='goal_0',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plan',
            name='goal_1',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plan',
            name='goal_2',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plan',
            name='goods',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='plan',
            name='name',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AddField(
            model_name='tag',
            name='plans',
            field=models.ManyToManyField(related_name='plan_tag', to='plan.Plan'),
        ),
    ]

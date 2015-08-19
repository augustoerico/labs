# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('in_date', models.DateField()),
                ('value', models.DecimalField(max_digits=12, decimal_places=2)),
            ],
        ),
        migrations.CreateModel(
            name='Laboratory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateField()),
                ('laboratory', models.ForeignKey(to='labs.Laboratory')),
            ],
        ),
        migrations.CreateModel(
            name='Responsible',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='responsible',
            field=models.ForeignKey(to='labs.Responsible'),
        ),
        migrations.AddField(
            model_name='budget',
            name='project',
            field=models.ForeignKey(to='labs.Project'),
        ),
    ]

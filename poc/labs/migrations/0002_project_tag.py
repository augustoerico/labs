# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='tag',
            field=models.CharField(default='2014-098881', max_length=30),
            preserve_default=False,
        ),
    ]

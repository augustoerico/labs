# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('labs', '0002_project_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='laboratory',
            name='responsibles',
            field=models.ManyToManyField(to='labs.Responsible'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0004_auto_20170825_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guest',
            name='plusones',
            field=models.PositiveIntegerField(),
        ),
    ]

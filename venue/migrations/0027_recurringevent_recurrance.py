# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0026_auto_20170922_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurringevent',
            name='recurrance',
            field=models.CharField(default='Weekly', max_length=7, verbose_name=b'Weekly or Monthly'),
            preserve_default=False,
        ),
    ]

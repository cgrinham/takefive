# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0024_auto_20170919_1258'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='source',
            field=models.CharField(default=b'internal', max_length=b'100'),
        ),
    ]

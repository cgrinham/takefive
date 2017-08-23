# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 23, 9, 49, 15, 293596, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venue',
            name='created',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 23, 9, 49, 25, 672037, tzinfo=utc), editable=False),
            preserve_default=False,
        ),
    ]

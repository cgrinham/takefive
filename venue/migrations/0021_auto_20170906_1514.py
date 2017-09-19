# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0020_auto_20170906_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membership',
            name='joined',
        ),
        migrations.AddField(
            model_name='membership',
            name='starts',
            field=models.DateField(default=datetime.datetime(2017, 9, 6, 15, 14, 12, 901405, tzinfo=utc), verbose_name=b'Date started'),
            preserve_default=False,
        ),
    ]

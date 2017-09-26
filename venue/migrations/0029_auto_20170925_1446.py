# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0028_auto_20170925_1300'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recurringevent',
            name='dateend',
        ),
        migrations.RemoveField(
            model_name='recurringevent',
            name='datestart',
        ),
        migrations.AddField(
            model_name='recurringevent',
            name='firstevent',
            field=models.DateField(default=datetime.date(2017, 9, 25), verbose_name=b'First Event Date'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='recurringevent',
            name='lastevent',
            field=models.DateField(default=datetime.date(2017, 9, 25), verbose_name=b'Last Event Date'),
            preserve_default=False,
        ),
    ]

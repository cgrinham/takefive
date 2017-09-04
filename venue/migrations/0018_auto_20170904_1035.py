# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0017_auto_20170830_1151'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='defaultplusones',
            field=models.PositiveIntegerField(default=5, verbose_name=b'Default max Plus Ones'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='venuelayout',
            name='description',
            field=models.CharField(max_length=400, blank=True),
        ),
    ]

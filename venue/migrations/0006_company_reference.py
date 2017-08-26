# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0005_auto_20170825_1501'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='reference',
            field=models.CharField(default='threewisemonkeys', max_length=40),
            preserve_default=False,
        ),
    ]

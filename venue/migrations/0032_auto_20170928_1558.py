# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0031_auto_20170928_1232'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='company',
            field=models.ForeignKey(blank=True, to='venue.Company', null=True),
        ),
    ]

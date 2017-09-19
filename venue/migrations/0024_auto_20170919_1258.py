# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0023_membershiptype_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershiptype',
            name='agerestriction',
            field=models.PositiveIntegerField(default=18),
        ),
        migrations.AlterField(
            model_name='membershiptype',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name=b'Hidden membership type'),
        ),
    ]

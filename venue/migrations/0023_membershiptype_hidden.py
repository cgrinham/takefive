# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0022_membershiptype_membershipopen'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershiptype',
            name='hidden',
            field=models.BooleanField(default=False, verbose_name=b'Hidden membership type'),
            preserve_default=False,
        ),
    ]

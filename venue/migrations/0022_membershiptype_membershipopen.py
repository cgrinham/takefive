# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0021_auto_20170906_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='membershiptype',
            name='membershipopen',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]

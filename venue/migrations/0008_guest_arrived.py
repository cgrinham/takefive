# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0007_venue_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='arrived',
            field=models.BooleanField(default=False),
        ),
    ]

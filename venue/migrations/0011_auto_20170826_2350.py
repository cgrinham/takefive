# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0010_event_capacity'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='capacity',
        ),
        migrations.AddField(
            model_name='venue',
            name='capacity',
            field=models.PositiveIntegerField(default=10, verbose_name=b'Venue Capacity'),
            preserve_default=False,
        ),
    ]

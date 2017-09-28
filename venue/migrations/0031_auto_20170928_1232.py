# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0030_auto_20170926_1428'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestlist',
            name='recurringevent',
            field=models.ForeignKey(blank=True, to='venue.RecurringEventDate', null=True),
        ),
        migrations.AlterField(
            model_name='guestlist',
            name='event',
            field=models.ForeignKey(blank=True, to='venue.Event', null=True),
        ),
    ]

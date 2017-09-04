# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0015_venuelayout_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuelayoutarea',
            name='company',
            field=models.ForeignKey(default=False, to='venue.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='venuelayoutarea',
            name='venue',
            field=models.ForeignKey(default=False, to='venue.Venue'),
            preserve_default=False,
        ),
    ]

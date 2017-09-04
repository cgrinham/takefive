# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0014_areahirebooking'),
    ]

    operations = [
        migrations.AddField(
            model_name='venuelayout',
            name='company',
            field=models.ForeignKey(default=False, to='venue.Company'),
            preserve_default=False,
        ),
    ]

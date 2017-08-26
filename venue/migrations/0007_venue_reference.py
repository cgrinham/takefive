# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0006_company_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='venue',
            name='reference',
            field=models.CharField(default='twisters', max_length=40),
            preserve_default=False,
        ),
    ]

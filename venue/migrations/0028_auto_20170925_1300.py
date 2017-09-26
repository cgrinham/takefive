# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0027_recurringevent_recurrance'),
    ]

    operations = [
        migrations.RenameField(
            model_name='recurringevent',
            old_name='recurrance',
            new_name='recurrence',
        ),
    ]

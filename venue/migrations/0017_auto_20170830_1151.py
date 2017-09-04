# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0016_auto_20170830_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='areahirebooking',
            name='company',
            field=models.ForeignKey(default=False, to='venue.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='areahirebooking',
            name='venue',
            field=models.ForeignKey(default=False, to='venue.Venue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='event',
            name='company',
            field=models.ForeignKey(default=False, to='venue.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guest',
            name='company',
            field=models.ForeignKey(default=False, to='venue.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guest',
            name='venue',
            field=models.ForeignKey(default=False, to='venue.Venue'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guestlist',
            name='company',
            field=models.ForeignKey(default=False, to='venue.Company'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='guestlist',
            name='venue',
            field=models.ForeignKey(default=False, to='venue.Venue'),
            preserve_default=False,
        ),
    ]

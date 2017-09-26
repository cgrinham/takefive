# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0029_auto_20170925_1446'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringEventDate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('datestart', models.DateField(verbose_name=b'Event Start Date')),
                ('timestart', models.TimeField(verbose_name=b'Event Start Time')),
                ('dateend', models.DateField(verbose_name=b'Event End Date')),
                ('timeend', models.TimeField(verbose_name=b'Event End Time')),
                ('company', models.ForeignKey(to='venue.Company')),
                ('event', models.ForeignKey(to='venue.RecurringEvent')),
                ('venue', models.ForeignKey(to='venue.Venue')),
            ],
        ),
        migrations.RemoveField(
            model_name='recurringeventdates',
            name='company',
        ),
        migrations.RemoveField(
            model_name='recurringeventdates',
            name='event',
        ),
        migrations.RemoveField(
            model_name='recurringeventdates',
            name='venue',
        ),
        migrations.DeleteModel(
            name='RecurringEventDates',
        ),
    ]

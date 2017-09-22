# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0025_guest_source'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecurringEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120, verbose_name=b'Event Name')),
                ('description', models.TextField(verbose_name=b'Description')),
                ('datestart', models.DateField(verbose_name=b'Event Start Date')),
                ('timestart', models.TimeField(verbose_name=b'Event Start Time')),
                ('dateend', models.DateField(verbose_name=b'Event End Date')),
                ('timeend', models.TimeField(verbose_name=b'Event End Time')),
                ('monday', models.BooleanField(verbose_name=b'Recurs on Mondays')),
                ('tuesday', models.BooleanField(verbose_name=b'Recurs on Tuesdays')),
                ('wednesday', models.BooleanField(verbose_name=b'Recurs on Wednesdays')),
                ('thursday', models.BooleanField(verbose_name=b'Recurs on Thursdays')),
                ('friday', models.BooleanField(verbose_name=b'Recurs on Fridays')),
                ('saturday', models.BooleanField(verbose_name=b'Recurs on Saturdays')),
                ('sunday', models.BooleanField(verbose_name=b'Recurs on Sundays')),
                ('company', models.ForeignKey(to='venue.Company')),
                ('venue', models.ForeignKey(to='venue.Venue')),
            ],
        ),
        migrations.CreateModel(
            name='RecurringEventDates',
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
            model_name='event',
            name='recurring',
        ),
    ]

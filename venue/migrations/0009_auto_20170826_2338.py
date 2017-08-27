# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0008_guest_arrived'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestlist',
            name='listopen',
            field=models.BooleanField(default=True, verbose_name=b'List Open?'),
        ),
        migrations.AddField(
            model_name='guestlist',
            name='maxguests',
            field=models.PositiveIntegerField(default=50, verbose_name=b'Maximum number of guests'),
        ),
        migrations.AlterField(
            model_name='event',
            name='dateend',
            field=models.DateField(verbose_name=b'Event End Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='datestart',
            field=models.DateField(verbose_name=b'Event Start Date'),
        ),
        migrations.AlterField(
            model_name='event',
            name='description',
            field=models.TextField(verbose_name=b'Description'),
        ),
        migrations.AlterField(
            model_name='event',
            name='name',
            field=models.CharField(max_length=120, verbose_name=b'Event Name'),
        ),
        migrations.AlterField(
            model_name='event',
            name='recurring',
            field=models.BooleanField(verbose_name=b'Recurring event'),
        ),
        migrations.AlterField(
            model_name='event',
            name='timeend',
            field=models.TimeField(verbose_name=b'Event End Time'),
        ),
        migrations.AlterField(
            model_name='event',
            name='timestart',
            field=models.TimeField(verbose_name=b'Event Start Time'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='arrived',
            field=models.BooleanField(default=False, verbose_name=b'Arrived'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='email',
            field=models.EmailField(max_length=254, verbose_name=b'Email'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='firstname',
            field=models.CharField(max_length=50, verbose_name=b'First Name'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='lastname',
            field=models.CharField(max_length=50, verbose_name=b'Last Name'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='member',
            field=models.BooleanField(verbose_name=b'Member'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='notes',
            field=models.CharField(max_length=140, verbose_name=b'Additional information'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='plusones',
            field=models.PositiveIntegerField(verbose_name=b'Plus Ones'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='timeslot',
            field=models.CharField(max_length=50, verbose_name=b'Time Slot'),
        ),
        migrations.AlterField(
            model_name='guestlist',
            name='name',
            field=models.CharField(max_length=100, verbose_name=b'Guest List Title'),
        ),
    ]

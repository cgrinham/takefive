# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('datestart', models.DateField()),
                ('timestart', models.TimeField()),
                ('dateend', models.DateField()),
                ('timeend', models.TimeField()),
                ('recurring', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='GuestList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('member', models.BooleanField()),
                ('timeslot', models.CharField(max_length=50)),
                ('plusones', models.IntegerField()),
                ('notes', models.CharField(max_length=140)),
                ('event', models.ForeignKey(to='venue.Event')),
            ],
        ),
        migrations.CreateModel(
            name='Venue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('owner', models.ForeignKey(to='venue.Company')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='venue',
            field=models.ForeignKey(to='venue.Venue'),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0012_auto_20170827_1518'),
    ]

    operations = [
        migrations.CreateModel(
            name='VenueLayout',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Default Layout', max_length=120)),
                ('description', models.CharField(max_length=400)),
                ('venue', models.ForeignKey(to='venue.Venue')),
            ],
        ),
        migrations.CreateModel(
            name='VenueLayoutArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40)),
                ('capacity', models.PositiveIntegerField()),
                ('notes', models.CharField(max_length=500)),
                ('price', models.PositiveIntegerField()),
                ('layout', models.ForeignKey(to='venue.VenueLayout')),
            ],
        ),
    ]

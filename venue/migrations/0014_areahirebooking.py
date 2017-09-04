# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0013_venuelayout_venuelayoutarea'),
    ]

    operations = [
        migrations.CreateModel(
            name='AreaHireBooking',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50, verbose_name=b'First Name')),
                ('lastname', models.CharField(max_length=50, verbose_name=b'Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email Address')),
                ('phone', models.CharField(blank=True, max_length=18, validators=[django.core.validators.RegexValidator(regex=b'^\\+?1?\\d{9,15}$', message=b"Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")])),
                ('area', models.ForeignKey(to='venue.VenueLayoutArea')),
            ],
        ),
    ]

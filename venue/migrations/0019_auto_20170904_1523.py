# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0018_auto_20170904_1035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50, verbose_name=b'First Name')),
                ('lastname', models.CharField(max_length=50, verbose_name=b'Last Name')),
                ('email', models.EmailField(max_length=254, verbose_name=b'Email')),
                ('dateofbirth', models.DateField(verbose_name=b'Date of Birth')),
                ('appearances', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Membership',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('joined', models.DateField(verbose_name=b'Date joined')),
                ('expires', models.DateField(verbose_name=b'Membership expiry date')),
                ('paid', models.BooleanField(default=False, verbose_name=b'Membership paid')),
                ('member', models.ForeignKey(to='venue.Member')),
                ('venue', models.ForeignKey(to='venue.Venue')),
            ],
        ),
        migrations.AlterField(
            model_name='guest',
            name='plusones',
            field=models.PositiveIntegerField(default=0, verbose_name=b'Plus Ones'),
        ),
    ]

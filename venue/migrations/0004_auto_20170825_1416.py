# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0003_auto_20170823_1206'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('member', models.BooleanField()),
                ('timeslot', models.CharField(max_length=50)),
                ('plusones', models.IntegerField()),
                ('notes', models.CharField(max_length=140)),
            ],
        ),
        migrations.RemoveField(
            model_name='guests',
            name='guestlist',
        ),
        migrations.AlterField(
            model_name='guestlist',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.DeleteModel(
            name='Guests',
        ),
        migrations.AddField(
            model_name='guest',
            name='guestlist',
            field=models.ForeignKey(to='venue.GuestList'),
        ),
    ]

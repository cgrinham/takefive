# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0002_auto_20170823_0949'),
    ]

    operations = [
        migrations.CreateModel(
            name='Guests',
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
            model_name='guestlist',
            name='firstname',
        ),
        migrations.RemoveField(
            model_name='guestlist',
            name='lastname',
        ),
        migrations.RemoveField(
            model_name='guestlist',
            name='member',
        ),
        migrations.RemoveField(
            model_name='guestlist',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='guestlist',
            name='plusones',
        ),
        migrations.RemoveField(
            model_name='guestlist',
            name='timeslot',
        ),
        migrations.AddField(
            model_name='guestlist',
            name='name',
            field=models.CharField(default=None, max_length=100),
        ),
        migrations.AlterField(
            model_name='company',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AlterField(
            model_name='venue',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False),
        ),
        migrations.AddField(
            model_name='guests',
            name='guestlist',
            field=models.ForeignKey(to='venue.GuestList'),
        ),
    ]

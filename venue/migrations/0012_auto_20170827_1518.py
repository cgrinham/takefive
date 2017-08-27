# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('venue', '0011_auto_20170826_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('company', models.ForeignKey(to='venue.Company')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='guestlist',
            name='maxplusones',
            field=models.PositiveIntegerField(default=1, verbose_name=b'Maximum plus ones a guest can bring'),
        ),
        migrations.AlterField(
            model_name='guest',
            name='notes',
            field=models.CharField(max_length=140, verbose_name=b'Additional information', blank=True),
        ),
    ]

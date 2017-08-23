# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=40)),
                ('dob', models.CharField(max_length=40)),
                ('email', models.EmailField(max_length=254)),
                ('signupdate', models.DateField()),
            ],
        ),
    ]

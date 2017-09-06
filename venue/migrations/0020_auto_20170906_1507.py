# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('venue', '0019_auto_20170904_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='MembershipType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=254)),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('length', models.CharField(max_length=10)),
                ('company', models.ForeignKey(to='venue.Company')),
                ('venue', models.ForeignKey(to='venue.Venue')),
            ],
        ),
        migrations.RemoveField(
            model_name='membership',
            name='venue',
        ),
        migrations.AlterField(
            model_name='member',
            name='appearances',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='membership',
            name='membershiptype',
            field=models.ForeignKey(default=True, to='venue.MembershipType'),
            preserve_default=False,
        ),
    ]

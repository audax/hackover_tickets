# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-27 16:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hackover_tickets', '0002_ticket_payed'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='accessed',
            field=models.BooleanField(default=False),
        ),
    ]

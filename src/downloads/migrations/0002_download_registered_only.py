# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-23 14:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='registered_only',
            field=models.BooleanField(default=True, verbose_name='only for registered users'),
        ),
    ]
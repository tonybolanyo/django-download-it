# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-30 11:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0002_auto_20170524_1714'),
    ]

    operations = [
        migrations.AlterField(
            model_name='download',
            name='file',
            field=models.FileField(upload_to='downloads', verbose_name='file'),
        ),
    ]
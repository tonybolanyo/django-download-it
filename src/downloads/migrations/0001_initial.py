# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-23 14:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Download',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('status', model_utils.fields.StatusField(choices=[('draft', 'draft'), ('published', 'published'), ('hidden', 'hidden')], default='draft', max_length=100, no_check_for_status=True, verbose_name='status')),
                ('status_changed', model_utils.fields.MonitorField(default=django.utils.timezone.now, monitor='status', verbose_name='status changed')),
                ('title', models.CharField(max_length=250, verbose_name='title')),
                ('slug', models.SlugField(unique=True, verbose_name='slug')),
                ('summary', models.TextField(blank=True, verbose_name='summary')),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('file', models.FileField(upload_to='downloads', verbose_name='file')),
                ('thumbnail', models.ImageField(upload_to='downloads', verbose_name='thumbnail')),
                ('downloads', models.IntegerField(default=0, verbose_name='download counter')),
            ],
            options={
                'verbose_name': 'download',
                'ordering': ('title',),
                'verbose_name_plural': 'downloads',
            },
        ),
    ]
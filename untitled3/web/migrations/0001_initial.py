# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-06-12 07:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hostName', models.CharField(max_length=255)),
                ('productName', models.CharField(max_length=255)),
                ('productSn', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('conn', models.ManyToManyField(to='web.Host')),
            ],
        ),
    ]

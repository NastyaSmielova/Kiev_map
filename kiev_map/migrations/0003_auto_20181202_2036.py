# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-12-02 18:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiev_map', '0002_auto_20181128_2144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='district',
            name='shortIntro',
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.AlterField(
            model_name='street',
            name='ism_id',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='street',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='street',
            name='shortIntro',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
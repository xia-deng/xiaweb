# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-13 16:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_auto_20161213_1644'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='column',
            field=models.ManyToManyField(to='article.Column', verbose_name='归属栏目'),
        ),
    ]

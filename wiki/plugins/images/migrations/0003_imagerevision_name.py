# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki_images', '0002_auto_20150910_2047'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagerevision',
            name='name',
            field=models.CharField(db_index=True, max_length=100, null=True, verbose_name='Image Name', blank=True),
        ),
    ]

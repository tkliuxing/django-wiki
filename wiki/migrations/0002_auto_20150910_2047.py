# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlerevision',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True),
        ),
        migrations.AlterField(
            model_name='revisionpluginrevision',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wiki_attachments', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachmentrevision',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True),
        ),
        migrations.AlterModelTable(
            name='attachment',
            table='wiki_attachments_attachment',
        ),
        migrations.AlterModelTable(
            name='attachmentrevision',
            table='wiki_attachments_attachmentrevision',
        ),
    ]

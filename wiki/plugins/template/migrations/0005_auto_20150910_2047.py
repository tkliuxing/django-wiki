# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('template', '0004_templaterevision_previous_revision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='current_revision',
            field=models.OneToOneField(related_name='current_set', null=True, to='template.TemplateRevision', blank=True, help_text='The revision of this template currently in use (on all articles using the template)', verbose_name='current revision'),
        ),
        migrations.AlterField(
            model_name='template',
            name='extend_to_children',
            field=models.BooleanField(default=False, help_text='You can extent this template to children articles.They will be able to use this template without import.', verbose_name='extend'),
        ),
        migrations.AlterField(
            model_name='template',
            name='reusableplugin_ptr',
            field=models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='wiki.ReusablePlugin'),
        ),
        migrations.AlterField(
            model_name='templaterevision',
            name='ip_address',
            field=models.GenericIPAddressField(verbose_name='IP address', null=True, editable=False, blank=True),
        ),
    ]

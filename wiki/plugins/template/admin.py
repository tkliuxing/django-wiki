from __future__ import unicode_literals
from __future__ import absolute_import
from django.contrib import admin

from . import models


class TemplateRevisionAdmin(admin.TabularInline):
    model = models.TemplateRevision
    extra = 1
    fields = ('template_content', 'user', 'user_message')


class TemplateAdmin(admin.ModelAdmin):

    inlines = [TemplateRevisionAdmin]

    # Do not let images be added in the admin. An image can only be added
    # from the article admin due to the automatic revision system.
    # def has_add_permission(self, request):
    #    return False

admin.site.register(models.Template, TemplateAdmin)

from __future__ import unicode_literals

from django.conf import settings as django_settings
from django import template

from wiki.core.plugins import registry as plugin_registry
from wiki.conf import settings
from wiki.plugins.languages.article_render import render

register = template.Library()

@register.inclusion_tag('wiki/plugins/languages/render.html', takes_context=True)
def wiki_languages_render(context, article, preview_content=None):
    if preview_content:
        content = render(article, context, preview_content=preview_content)
    else:
        content = None
    context.update({
        'article': article,
        'content': content,
        'preview': not preview_content is None,
        'plugins': plugin_registry.get_plugins(),
        'STATIC_URL': django_settings.STATIC_URL,
        'CACHE_TIMEOUT': settings.CACHE_TIMEOUT,
    })
    return context

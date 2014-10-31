from __future__ import unicode_literals

import markdown

from django.utils.safestring import mark_safe

from wiki.core.plugins import registry as plugin_registry
from wiki.conf import settings


class ArticleMarkdown(markdown.Markdown):
    
    def __init__(self, article, request, *args, **kwargs):
        kwargs = settings.MARKDOWN_KWARGS
        kwargs['extensions'] = kwargs.get('extensions', [])
        kwargs['extensions'] += plugin_registry.get_markdown_extensions()
        markdown.Markdown.__init__(self, *args, **kwargs)
        self.article = article
        self.request = request


def article_markdown(text, article, request, *args, **kwargs):
    md = ArticleMarkdown(article, request, *args, **kwargs)
    return md.convert(text)


def render(article, context, preview_content=None):
    print(context.get("LANGUAGE_CODE"))
    if not article.current_revision:
        return ""
    if preview_content:
        content = preview_content
    else:
        content = article.current_revision.content
    return mark_safe(article_markdown(content, article))

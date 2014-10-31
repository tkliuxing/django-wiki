# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals

from django.db import models
from django.conf import settings as dj_settings
from django.utils.translation import ugettext_lazy as _
from django.utils.safestring import mark_safe

from . import settings

from wiki import managers
from wiki.models.pluginbase import RevisionPlugin, RevisionPluginRevision
from wiki.models.article import Article, ArticleRevision
from wiki.core import article_markdown


class ArticleLanguage(models.Model):
    origin_language = models.CharField(max_length=10, choices=dj_settings.LANGUAGES)
    article = models.OneToOneField('wiki.Article', on_delete=models.CASCADE, 
                                verbose_name=_("article"))
    class Meta:
        verbose_name = _('article language')
        verbose_name_plural = _('article language')
        if settings.APP_LABEL:
            app_label = settings.APP_LABEL


class MultilingualArticle(Article):

    language = models.CharField(max_length=10, choices=dj_settings.LANGUAGES)
    main_article = models.ForeignKey('wiki.Article', on_delete=models.CASCADE, 
                                verbose_name=_("article"), related_name="sub_lang_articles")

    class Meta:
        verbose_name = _('language article')
        verbose_name_plural = _('language article')
        if settings.APP_LABEL:
            app_label = settings.APP_LABEL
        unique_together = (
            ('main_article', 'language'),
        )

    def render(self, preview_content=None):
        if not self.current_revision:
            return ""
        if preview_content:
            content = preview_content
        else:
            content = self.current_revision.content
        return mark_safe(article_markdown(content, self))

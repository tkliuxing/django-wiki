# -*- coding: utf-8 -*-
from django.utils.translation import ugettext as _
from django.conf.urls import patterns, url, include

from wiki.core.plugins import registry
from wiki.core.plugins.base import BasePlugin
from wiki.plugins.languages import settings
from wiki.plugins.languages import models
from wiki.plugins.languages import views

from wiki.plugins.languages.markdown_extensions import LanguagesExtension

from wiki.plugins.notifications.settings import ARTICLE_EDIT
from wiki.plugins.notifications.util import truncate_title
from wiki.plugins.languages import article_render


class LanguagesPlugin(BasePlugin):

    slug = 'languages'
    urlpatterns = {
        'article': patterns('',
            url('', include('wiki.plugins.languages.urls')),
        )
    }

    article_tab = (_('Languages'), "icon-leaf")
    article_view = views.LanguageView().dispatch

    def __init__(self):
        pass

registry.register(LanguagesPlugin)

from wiki.views.article import ArticleView
ArticleView.template_name = "wiki/plugins/languages/view.html"

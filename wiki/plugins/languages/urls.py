from django.conf.urls import patterns, url

from wiki.plugins.template import views
from wiki.plugins.languages import views as lview

urlpatterns = patterns('',
    url(r'^$',
        lview.LanguageView.as_view(),
        name='languages_index'
    ),
    url(r'^create/$',
        views.TemplateCreateView.as_view(),
        name='languages_create'
    ),
    url(r'^search/$',
        views.TemplateSearchView.as_view(),
        name='languages_search'
    ),
    url(r'^(?P<languages_id>\d+)/add/to/article/$',
        views.TemplateAddView.as_view(),
        name='languages_add_to_article'
    ),
    url(r'^history/(?P<languages_id>\d+)/$',
        views.TemplateHistoryView.as_view(),
        name='languages_history'
    ),
    url(r'^delete/(?P<languages_id>\d+)/$',
       views.TemplateDeleteView.as_view(),
       name='languages_delete'
    ),
    url(r'^change/(?P<languages_id>\d+)/revision/(?P<revision_id>\d+)/$',
       views.TemplateChangeRevisionView.as_view(),
       name='languages_revision_change'
    ),
    url(r'^json/query-title/$',
        views.QueryTitle.as_view(),
        name='languages_query_title'
    ),
    url('^(?P<languages_id>\d+)/revision/add/$',
        views.RevisionAddView.as_view(),
        name='languages_add_revision'
    ),
    url('^(?P<languages_id>\d+)/revision/add/preview/$',
        views.EditPreview.as_view(),
        name='languages_add_revision_preview'
    ),
    url('^create/preview/$',
        views.CreatePreview.as_view(),
        name='languages_create_preview'
    ),
)

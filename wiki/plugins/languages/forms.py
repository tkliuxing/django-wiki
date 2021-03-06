# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django import forms
from django.conf import settings as dj_settings
from django.utils.translation import ugettext as _

from wiki.editors import getEditor
from wiki.plugins.template import models
from wiki.forms import SpamProtectionMixin


class TemplateForm(forms.ModelForm):

    template_title = forms.SlugField(
        label=_('Template title'),
        required=True,
        help_text=_(
            'Use only alphanumeric characters and - or _. '
            'Note that you cannot change the title after creating the template.'
        ),
    )

    def __init__(self, *args, **kwargs):
        self.article = kwargs.pop('article', None)
        self.request = kwargs.pop('request', None)
        self.template = kwargs.pop('template', None)
        super(TemplateForm, self).__init__(*args, **kwargs)

    def clean_template_title(self):
        title = self.cleaned_data['template_title']
        if self.template and self.template.template_title:
            return self.template.template_title
        if models.Template.objects.filter(template_title=title):
            raise forms.ValidationError(
                _('A template named "%s" already exists.') % title
            )
        return title

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit', True)
        template_revision = super(TemplateForm, self).save(commit=False)

        if not self.template:
            template = models.Template()
            template.article = self.article
            template.template_title = self.cleaned_data['template_title']
            if commit:
                template.save()
            template.articles.add(self.article)
        else:
            template = self.template
        template_revision.template = template
        template_revision.set_from_request(self.request)
        if commit:
            template_revision.save()
        return template_revision

    class Meta:
        model = models.TemplateRevision
        fields = ('template_title', 'template_content', 'description',)
        widgets = {
            'template_content': getEditor().get_widget(),
            'description': forms.TextInput(),
        }

class CreateForm(forms.Form, SpamProtectionMixin):
    
    language = forms.CharField(label=_('Language'))
    title = forms.CharField(label=_('Title'),)
    content = forms.CharField(label=_('Contents'),
                              required=False, widget=getEditor().get_widget()) #@UndefinedVariable
    
    summary = forms.CharField(label=_('Summary'), help_text=_("Write a brief message for the article's history log."),
                              required=False)

    def __init__(self, main_article, *args, **kwargs):
        choices = dict(dj_settings.LANGUAGES)
        has_languages = main_article.sub_lang_articles.all().value_list('language', flat=True)
        for lang in has_languages:
            if choices.has_key(lang):
                choices.pop(lang)
        choices = list(choices)
        choices.sort()
        self.fields['language'].choices = choices


class RevisionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        self.template = kwargs.pop('template')
        super(RevisionForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        template_revision = super(RevisionForm, self).save(commit=False)
        template = self.template
        template_revision.template = template
        template_revision.set_from_request(self.request)
        template_revision.save()
        template.current_revision = template_revision
        template.save()
        return template_revision

    class Meta:
        model = models.TemplateRevision
        fields = ('template_content', 'description',)
        widgets = {
            'template_content': getEditor().get_widget(),
            'description': forms.TextInput(),
        }


class DeleteForm(forms.Form):

    """This form is both used for dereferencing and deleting template"""
    confirm = forms.BooleanField(label=_('Yes I am sure...'),
                                 required=False)

    def clean_confirm(self):
        if not self.cleaned_data['confirm']:
            raise forms.ValidationError(_('You are not sure enough!'))
        return True


class SearchForm(forms.Form):

    query = forms.CharField(
        label="", widget=forms.TextInput(attrs={'class': 'search-query'}),)

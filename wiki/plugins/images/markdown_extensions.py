from __future__ import absolute_import
from __future__ import unicode_literals
# -*- coding: utf-8 -*-
import markdown
import re

from os import path as os_path

from django.template.loader import render_to_string
from django.template import Context

IMAGE_RE = re.compile(
    r'.*(\[image\:(?P<id>\d+)(\s+align\:(?P<align>right|left))?\s*\]).*',
    re.IGNORECASE)

from wiki.plugins.images import models


class ImageExtension(markdown.Extension):

    """ Images plugin markdown extension for django-wiki. """

    def __init__(self, configs={}):
        # set extension defaults
        self.config = {
            'base_url': [
                '/',
                'String to append to beginning of URL.'],
            'html_class': [
                'wikiimage',
                'CSS hook. Leave blank for none.'],
            'default_level': [
                2,
                'The level that most articles are created at. Relative links will tend to start at that level.']}

        # Override defaults with user settings
        for key, value in configs:
            # self.config[key][0] = value
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        """ Insert ImagePreprocessor before ReferencePreprocessor. """
        self.md = md
        IMAGELINK_RE = r'!\[(?P<linkTitle>[^\]]+?)\]\(image:(?P<imageTitle>[a-zA-Z\d\._ -]+?)\)(?:\(wiki:(?P<wikiLink>[a-zA-Z\d\./_ -]*?)\))?'
        imagelinkPattern = ImageLinks(IMAGELINK_RE, self.getConfigs())
        imagelinkPattern.md = md
        md.inlinePatterns.add('imagelink', imagelinkPattern, "<image_link")
        md.preprocessors.add('dw-images', ImagePreprocessor(md), '>html_block')


class ImageLinks(markdown.inlinepatterns.Pattern):

    def __init__(self, pattern, config, **kwargs):
        markdown.inlinepatterns.Pattern.__init__(self, pattern, **kwargs)
        self.config = config

    def handleMatch(self, m):
        base_url, html_class = self._getMeta()
        link_title = m.group('linkTitle')
        wiki_link = m.group('wikiLink')
        path = os_path.join(base_url, wiki_link)

        image = None
        image_title = m.group('imageTitle')
        try:
            image = models.ImageRevision.objects.filter(plugin_set__isnull=False, name=image_title)[0]
        except:
            pass
        div = markdown.util.etree.Element('div')
        div.set('class', html_class)
        a1 = markdown.util.etree.Element('a')
        a1.set('href', path)
        a1.set('title', link_title)
        img = markdown.util.etree.Element('img')
        if image:
            img.set('alt', image.name + " Icon")
            img.set('src', image.image.url)
        else:
            img.set('alt', "Icon")
            img.set('src', '/favicon.ico')
        img.set('width', '36')
        img.set('height', '36')
        a1.append(img)
        div.append(a1)
        span = markdown.util.etree.Element('span')
        span.set('class', 'starbound')
        span_blank = markdown.util.etree.Element('span')
        span_blank.text = "&nbsp;"
        div.append(span_blank)
        a2 = markdown.util.etree.Element('a')
        a2.set('href', path)
        a2.set('title', link_title)
        a2.text = link_title
        div.append(a2)
        return div

    def _getMeta(self):
        """ Return meta data or config data. """
        base_url = self.config['base_url']
        html_class = self.config['html_class']
        if hasattr(self.md, 'Meta'):
            if 'wiki_base_url' in self.md.Meta:
                base_url = self.md.Meta['wiki_base_url'][0]
            if 'wiki_html_class' in self.md.Meta:
                html_class = self.md.Meta['wiki_html_class'][0]
        return base_url, html_class


class ImagePreprocessor(markdown.preprocessors.Preprocessor):

    """django-wiki image preprocessor - parse text for [image:id align:left|right|center] references. """

    def run(self, lines):
        new_text = []
        previous_line = ""
        line_index = None
        previous_line_was_image = False
        image = None
        image_id = None
        alignment = None
        caption_lines = []
        for line in lines:
            m = IMAGE_RE.match(line)
            if m:
                previous_line_was_image = True
                image_id = m.group('id').strip()
                alignment = m.group('align')
                try:
                    image = models.Image.objects.get(
                        article=self.markdown.article,
                        id=image_id,
                        current_revision__deleted=False)
                except models.Image.DoesNotExist:
                    pass
                line_index = line.find(m.group(1))
                line = line.replace(m.group(1), "")
                previous_line = line
                caption_lines = []
            elif previous_line_was_image:
                if line.startswith("    "):
                    caption_lines.append(line[4:])
                    line = None
                else:
                    caption_placeholder = "{{{IMAGECAPTION}}}"
                    html = render_to_string(
                        "wiki/plugins/images/render.html",
                        Context(
                            {'image': image, 'caption': caption_placeholder,
                             'align': alignment}))
                    html_before, html_after = html.split(caption_placeholder)
                    placeholder_before = self.markdown.htmlStash.store(
                        html_before,
                        safe=True)
                    placeholder_after = self.markdown.htmlStash.store(
                        html_after,
                        safe=True)
                    new_line = placeholder_before + "\n".join(
                        caption_lines) + placeholder_after + "\n"
                    previous_line_was_image = False
                    if previous_line is not "":
                        if previous_line[line_index:] is not "":
                            new_line = new_line[0:-1]
                        new_text[-1] = (previous_line[0:line_index] +
                                        new_line +
                                        previous_line[line_index:] +
                                        "\n" +
                                        line)
                        line = None
                    else:
                        line = new_line + line
            if line is not None:
                new_text.append(line)
        return new_text

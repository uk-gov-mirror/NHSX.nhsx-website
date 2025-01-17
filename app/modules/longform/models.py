# stdlib
import logging
import lxml.html
from collections import Counter

# 3rd party
from django.db import models
from wagtail.core import fields
from taggit.models import TaggedItemBase
from wagtail.search import index
from dal_select2.widgets import ModelSelect2Multiple
from modelcluster.fields import ParentalKey
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.utils.decorators import cached_classmethod
from modelcluster.contrib.taggit import ClusterTaggableManager
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from django.views.decorators.cache import cache_page
from django.utils.text import slugify

# Project
from modules.core.models.abstract import (
    BasePage,
    BaseIndexPage,
    CanonicalMixin,
    PageAuthorsMixin,
)


logger = logging.getLogger(__name__)


def slug_count_text(number):
    if number == 1:
        return ""
    else:
        return "-" + str(number)


################################################################################
# Page models
################################################################################


class LongformPost(BasePage, PageAuthorsMixin, CanonicalMixin):
    # standard approach appears to be
    # (via https://docs.wagtail.io/en/latest/topics/streamfield.html)
    # author = models.Charfield(max_length=255)
    # which also gives subcategories for StreamField
    parent_page_types = ["LongformPostIndexPage"]
    subpage_types = []
    updated_at = models.DateTimeField(
        editable=True,
        null=True,
        blank=True,
        verbose_name="Updated at (leave blank for initial publication)",
    )
    history = RichTextField(
        blank=True, verbose_name="Version history (leave blank for initial publication)"
    )

    content_panels = [
        *Page.content_panels,
        FieldPanel("first_published_at"),
        FieldPanel("updated_at"),
        StreamFieldPanel("body"),
        FieldPanel("history"),
    ]

    settings_panels = CanonicalMixin.panels + BasePage.settings_panels

    def replace_headers(self, html):
        """Given a html string, return a html string where the header tags
        have id attributes so they can be used as anchors, and list the ids
        and text of those tags so we can make a table of contents."""
        header_tags = ["h2"]
        toc = []
        root = lxml.html.fromstring(html)
        for tag_name in header_tags:
            for tag in root.xpath(f"//{tag_name}"):
                # create a slugged name for the tag of the form tag-text-3
                header_name = tag.text
                bare_slug = slugify(header_name, allow_unicode=True)
                self.slug_count[bare_slug] += 1
                slug = bare_slug + slug_count_text(self.slug_count[bare_slug])
                # modify the tag and record the details
                tag.set("id", slug)
                toc.append((header_name, slug))
        return lxml.html.tostring(root).decode("utf-8"), toc

    def get_context(self, request):
        """Pass the html of each richtext node within the streamfield to
        replace_headers, creating a page-wide table of contents. We use
        self.slug_count to preserve the list of slugs seen so far across
        multiple rich_text blocks."""
        context = super().get_context(request)
        context["toc"] = []  # table of contents
        self.slug_count = Counter()
        for i, block in enumerate(self.body._raw_data):
            # TODO consider diving deeper into expander nodes
            if block["type"] == "rich_text":
                replacement_html, new_toc = self.replace_headers(block["value"])
                context["toc"].extend(new_toc)
                self.body._raw_data[i]["value"] = replacement_html
        return context


class LongformPostIndexPage(BaseIndexPage):
    _child_model = LongformPost

    subpage_types = ["LongformPost"]
    max_count = 1

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Rss201rev2Feed

from blog.models import Article

class ExtendedRssFeed(Rss201rev2Feed):
    """
    Rss feed with content
    """
    mime_type = 'application/xml'

    def root_attributes(self):
        attrs = super(ExtendedRssFeed, self).root_attributes()
        attrs['xmlns:content'] = 'http://purl.org/rss/1.0/modules/content/'
        return attrs

    def add_item_elements(self, handler, item):
        super(ExtendedRssFeed, self).add_item_elements(handler, item)
        handler.addQuickElement(u'content:encoded', item['content_encoded'])


class BlogPostFeed(Feed):
    feed_type = ExtendedRssFeed
    title = "Django blog"
    link = "/blog/rss"
    description = "Update on Django blog's articles."

    def items(self):
        return Article.objects.filter(status='p')[:10]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return item.abstract or '没有简介, 请去看原文吧'

    def item_pubdate(self, item):
        return item.publish_time

    def item_extra_kwargs(self, item):
        return {'content_encoded': self.item_content_encoded(item)}

    def item_content_encoded(self, item):
        return item.body
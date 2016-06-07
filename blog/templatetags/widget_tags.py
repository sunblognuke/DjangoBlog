from django import template
from django.db.models import Count

register = template.Library()

from blog.models import Article, Category

@register.inclusion_tag('widget/recent_entries.html')
def get_recent_entries(number=5, template='widget/recent_entries.html'):
    """
    Return the most recent entries.
    """
    return {'entries': Article.objects.filter(status='p')[:number]}


@register.inclusion_tag('widget/random_entries.html')
def get_random_entries(number=5, template='widget/random_entries.html'):
    """
    Return random entries.
    """
    return {'template': template,
            'entries': Article.objects.filter(status='p').order_by('?')[:number]}


@register.inclusion_tag('widget/categories.html', takes_context=True)
def get_categories(context, template='widget/categories.html'):
    """
    Return the published categories.
    """
    return {'template': template,
            'categories': Category.published.all().annotate(
                count_article_published=Count('article')),
            'context_category': context.get('category')}

# @register.inclusion_tag('zinnia/tags/dummy.html')
# def get_popular_entries(number=5, template='zinnia/tags/entries_popular.html'):
#     """
#     Return popular entries.
#     """
#     return {'template': template,
#             'entries': Entry.published.filter(
#                 comment_count__gt=0).order_by(
#                 '-comment_count', '-publication_date')[:number]}


# @register.inclusion_tag('zinnia/tags/dummy.html', takes_context=True)
# def get_similar_entries(context, number=5,
#                         template='zinnia/tags/entries_similar.html'):
#     """
#     Return similar entries.
#     """
#     entry = context.get('entry')
#     if not entry:
#         return {'template': template, 'entries': []}

#     vectors = EntryPublishedVectorBuilder()
#     entries = vectors.get_related(entry, number)

#     return {'template': template,
#             'entries': entries}
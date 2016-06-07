# -*- coding: utf-8 -*-
from django.db import models

def entries_published(queryset):
    """
    Return only the entries published.
    """
    # now = timezone.now()
    return queryset.filter(
        # models.Q(start_publication__lte=now) |
        # models.Q(start_publication=None),
        # models.Q(end_publication__gt=now) |
        # models.Q(end_publication=None),
        status='p')

class EntryPublishedManager(models.Manager):
    """
    Manager to retrieve published entries.
    """

    def get_queryset(self):
        """
        Return published entries.
        """
        return entries_published(
            super(EntryPublishedManager, self).get_queryset())


class EntryRelatedPublishedManager(models.Manager):
    """
    Manager to retrieve objects associated with published articles.
    """

    def get_queryset(self):
        """
        Return a queryset containing published articles.
        """
        return super(
            EntryRelatedPublishedManager, self).get_queryset().filter(
            article__status='p'
            ).distinct()


class ArchivesManager(models.Manager):
    def get_queryset(self):
        return Article.objects.datetimes('publish_time','month',order='DESC')
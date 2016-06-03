# -*- coding: utf-8 -*-
import datetime
import re

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.template.defaultfilters import slugify

from simplemde.fields import SimpleMDEField

# Create your models here.
@python_2_unicode_compatible
class ArchivesManager(models.Manager):
    def get_queryset(self):
        return Article.objects.datetimes('publish_time','month',order='DESC')


class ArchivesItem(models.Model):
    archives = ArchivesManager()

    # def get_absolute_url(self):
    #     return reverse('blog:monthly_archives’', args=(self.archives.year, self.archives.strftime('%b').lower()))
    #     # return ('blog:monthly_archives’', None, {
    #     #     'year': self.year,
    #     #     'month': self.strftime('%b').lower()
    #     # })

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', "草稿"),
        ('p', "已发布"),
    )

    title = models.CharField('标题', max_length=100)
    # body = models.TextField('正文')
    body = SimpleMDEField(verbose_name=u'')

    cover = models.URLField('封面图片', default='', blank=True)
    abstract = models.TextField('摘要', max_length=220, blank=True, null=True, help_text="可选，如若为空将摘取正文的前220个字符")
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now_add=True)
    publish_time  = models.DateTimeField('发表时间', default=datetime.datetime.now, null=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES)
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    recommended = models.BooleanField(verbose_name='推荐', default=False)
    public = models.BooleanField(verbose_name='公开', default=True)
    topped = models.BooleanField(verbose_name='置顶', default=False)

    category = models.ForeignKey('Category', verbose_name='所属分类', null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', null=True, blank=True, help_text='标签')

    slug = models.SlugField('slug', unique=True, max_length=100, help_text="Cool URIs dont change")

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail', args=(self.id, self.slug))

    def save(self, *args, **kwargs):
        self.abstract = self.abstract or self.body[:220]
        modified = kwargs.pop("modified", True)
        if modified:
            self.last_modified_time = datetime.datetime.utcnow()

        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-publish_time']
        verbose_name = '文章列表'
        verbose_name_plural = '文章列表'


class Tag(models.Model):
    name = models.CharField('名称', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        verbose_name = '标签集合'
        verbose_name_plural = '标签集合'

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField('名称', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)


    class Meta:
        verbose_name = '分类目录'
        verbose_name_plural = '分类目录'


    def __str__(self):
        return self.name

class Friend(models.Model):
    """
    友情链接
    """
    title = models.CharField('名称', max_length=100, default='')
    url = models.URLField('链接', default='')
    position = models.SmallIntegerField('位置', default=1)
    active = models.BooleanField('是否激活', default=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'

    def __str__(self):
        return self.title
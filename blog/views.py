from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from blog.models import Article, Category, Tag
import markdown2

# Create your views here.
class IndexView(ListView):  # 首页视图
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(IndexView, self).get_context_data(**kwargs)

class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self, queryset=None):
        obj = super(ArticleDetailView, self).get_object()
        # 阅读数增1
        obj.views += 1
        obj.save(modified=False)

        obj.body = markdown2.markdown(obj.body, extras=['fenced-code-blocks'], )
        
        return obj

class CategoryView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(CategoryView, self).get_context_data(**kwargs)

class TagView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        query_condition = {
            'status': 'p',
            #'is_public': True
        }

        if 'tag_name' in self.kwargs:
            query_condition['tags__name'] = self.kwargs['tag_name']

        article_list = Article.objects.filter(**query_condition)
        for article in article_list:
            article.body = markdown2.markdown(article.body)
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['Tag_list'] = Tag.objects.all().order_by('name')
        return super(TagView, self).get_context_data(**kwargs)

class ArchiveView(ListView):
    template_name = "blog/archive.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')

        # for article in article_list:
        #     article.body = markdown2.markdown(article.body)

        return article_list

class MonthlyArchivesView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(publish_time__year=self.kwargs['year'], publish_time__month=self.kwargs['month'])
        for article in article_list:
            article.body = markdown2.markdown(article.body, extras=['fenced-code-blocks'], )

        return article_list
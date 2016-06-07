from django.contrib import admin

# Register your models here.
from blog.models import Article, Category, Friend
from blog.forms import ArticleForm

# Add in this class to customized the Admin Interface 
class ArticleAdmin(admin.ModelAdmin): 
	list_display = ('title', 'category', 'status', 'publish_time', 'views')
	list_filter  = ('category', 'publish_time', 'status')
	# 指定显示编辑的字段，其余则隐藏
	# fields = (
	#     'title',
	#     'slug',
	#     'cover',
	#     'body',
	#     'abstract',
	#     'status',
	#     ('topped', 'public', 'recommended'),
	#     'publish_time',
	#     'category',
	#     'tags'
	# )

	# alternative way as above
	fieldsets = [
				(None, {'fields': 
				['title',
				'slug',
		        'cover',
		        'body',
		        'abstract',
		        'status',
		        'publish_time',
		        'category',
		        'tags',]}),
	            ('文章选项', {'fields':[('topped', 'public', 'recommended')]})
	           ]

	search_fields = ('title', 'body', )
	prepopulated_fields = {'slug':('title',)}
	list_per_page = 20
	actions = ['make_published']
	form = ArticleForm

	def make_published(self, request, queryset):
		rows_updated = 0
		for entry in queryset:
		    entry.status = 'p'
		    rows_updated += 1
		    if entry.publish_time is None:
		        entry.publish_time = datetime.datetime.now()
		    entry.save()
		message_bit = "%s 篇博客 " % rows_updated
		self.message_user(request, "%s 成功发布" % message_bit)

	
	make_published.short_description = "立即发表"

# Update the registeration to include this customised interface 
admin.site.register(Article, ArticleAdmin)

class FriendAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'position', 'active')

admin.site.register(Friend, FriendAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )

admin.site.register(Category, CategoryAdmin)
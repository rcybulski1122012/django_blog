from django.contrib import admin

from blog.models import Post, Comment, Category
from blog.views import redis_connection


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'published', 'likes', 'number_of_views')
    list_filter = ('created', 'published')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['publish_selected', 'hide_selected']

    @staticmethod
    def number_of_views(obj):
        views = redis_connection.get(f'post:{obj.id}:views')
        if views is not None:
            return int(views)
        else:
            return 0

    @staticmethod
    def publish_selected(modeladmin, request, queryset):
        queryset.update(published=True)

    @staticmethod
    def hide_selected(modeladmin, request, queryset):
        queryset.update(published=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content')
    list_filter = ('post',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

from django.contrib import admin

from blog.models import Post, Comment, Category
from blog.views import r


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'published', 'number_of_likes')
    list_filter = ('created', 'published')
    prepopulated_fields = {'slug': ('title',)}
    actions = ['publish_selected', 'hide_selected']

    @staticmethod
    def number_of_likes(obj):
        likes = r.get(f'post:{obj.id}:likes')
        if likes is not None:
            return int(likes)
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



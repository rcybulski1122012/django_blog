from django.contrib import admin

from blog.models import Post, Comment, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'is_published', 'likes', 'number_of_views')
    list_filter = ('created', 'is_published', 'category')
    prepopulated_fields = {'slug': ('title',)}
    actions = ('publish_selected', 'hide_selected')

    @staticmethod
    def publish_selected(modeladmin, request, queryset):
        queryset.update(is_published=True)

    @staticmethod
    def hide_selected(modeladmin, request, queryset):
        queryset.update(is_published=False)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content')
    list_filter = ('post',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

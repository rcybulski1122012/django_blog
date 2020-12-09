from django.contrib import admin

from blog.models import Post, Comment, Category


def publish_selected(modeladmin, request, queryset):
    queryset.update(published=True)


def hide_selected(modeladmin, request, queryset):
    queryset.update(published=False)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'published')
    list_filter = ('created', 'published')
    prepopulated_fields = {'slug': ('title',)}
    actions = [publish_selected, hide_selected]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'content')
    list_filter = ('post',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}



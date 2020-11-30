from django.contrib import admin

from blog.models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created', 'published')
    list_filter = ('created', 'published')
    prepopulated_fields = {'slug': ('title',)}

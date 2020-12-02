from django.db import models
from django.urls import reverse

from martor.models import MartorField


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content = MartorField()
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[self.slug])


class Comment(models.Model):
    author = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.content

from django.contrib.postgres.search import TrigramSimilarity
from django.db import models
from django.db.models import F
from django.urls import reverse

from martor.models import MartorField

from blog.views_counter import PostViewsCounter


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'<Category: {self.name}>'
    

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True)

    def get_similar(self, title, *, similarity=0.3):
        return self.annotate(similarity=TrigramSimilarity('title', title),).filter(
            similarity__gt=similarity).order_by('-similarity')


class Post(models.Model):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    content = MartorField()
    description = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)

    objects = PostQuerySet().as_manager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._views_counter = PostViewsCounter(self)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

    def __repr__(self):
        return f'<Post: {self.title}>'

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    @property
    def number_of_views(self):
        return self._views_counter.get_number_of_views()

    def increment_views_counter(self):
        self._views_counter.increment()

    def like(self, request):
        if self.is_liked(request):
            self._unlike(request)
        else:
            self._like(request)
        self.save()
        self.refresh_from_db()

    def _like(self, request):
        self.likes = F('likes') + 1
        request.session[f'like-{self.pk}'] = True

    def _unlike(self, request):
        self.likes = F('likes') - 1
        request.session[f'like-{self.pk}'] = False

    def is_liked(self, request):
        return request.session.get(f'like-{self.pk}', False)


class Comment(models.Model):
    author = models.CharField(max_length=50)
    content = models.TextField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True, blank=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.content

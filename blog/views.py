from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class PostDetailView(DetailView):
    model = Post


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.annotate(
        similarity=TrigramSimilarity('title', query),
    ).filter(similarity__gt=0.3, published=True).order_by('-similarity')
    return render(request, 'blog/search.html', {'query': query, 'posts': posts})

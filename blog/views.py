from django.contrib.postgres.search import TrigramSimilarity
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView

from blog.forms import CommentForm
from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form})


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.annotate(
        similarity=TrigramSimilarity('title', query),
    ).filter(similarity__gt=0.3, published=True).order_by('-similarity')
    return render(request, 'blog/search.html', {'query': query, 'posts': posts})

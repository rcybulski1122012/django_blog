# from django.shortcuts import render
from django.views.generic import ListView, DetailView

from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'

    def get_queryset(self):
        return super().get_queryset().filter(published=True)


class PostDetailView(DetailView):
    model = Post

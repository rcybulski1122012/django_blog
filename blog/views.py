from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView
from django.conf import settings

from blog.forms import CommentForm
from blog.models import Post, Category
from common.decorators import ajax_required


def post_list(request):
    category_slug = request.GET.get('c', None)
    posts = Post.objects.published()
    page = request.GET.get('page')
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    posts = _get_posts_for_page(paginator, page)

    if request.is_ajax():
        return _render_post_list_ajax(request, posts, page, paginator)
    else:
        return _render_post_list(request, posts)


def _get_posts_for_page(paginator, page):
    try:
        return paginator.page(page)
    except PageNotAnInteger:
        return paginator.page(1)
    except EmptyPage:
        return paginator.page(paginator.num_pages)


def _render_post_list(request, posts):
    return render(request, 'blog/post_list.html', {'posts': posts})


def _render_post_list_ajax(request, posts, page, paginator):
    if int(page) > paginator.num_pages:
        return HttpResponse('')
    else:
        return render(request, 'blog/post_ajax.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.published(), slug=slug)
    post.increment_views_counter()
    is_liked = post.is_liked(request)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save_with_post(post)
            return redirect(reverse('blog:post_detail', args=[post.slug]))
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form, 'is_liked': is_liked})


@ajax_required
def post_like(request):
    try:
        post_id = int(request.POST.get('post_id'))
    except (TypeError, ValueError):
        raise Http404('Invalid value for post_id')
    post = get_object_or_404(Post.objects.published(), id=post_id)
    post.like(request)
    return HttpResponse(post.likes)


def search(request):
    query = request.GET.get('query', '')
    posts = Post.objects.published().get_similar(title=query)
    return render(request, 'blog/search.html', {'query': query, 'posts': posts})


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'


def top_posts(request):
    top_viewed_posts = _get_top_5_viewed_posts()

    top_liked_posts = _get_top_5_liked_posts()
    return render(request, 'blog/top_posts.html', {'top_viewed_posts': top_viewed_posts,
                                                   'top_liked_posts': top_liked_posts})


def _get_top_5_liked_posts():
    return Post.objects.published().order_by('-likes')[:5]


def _get_top_5_viewed_posts():
    top_viewed_posts = list(Post.objects.published())
    top_viewed_posts.sort(key=lambda x: x.number_of_views, reverse=True)
    top_viewed_posts = top_viewed_posts[:5]
    return top_viewed_posts

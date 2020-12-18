from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView, ListView
from django_redis import get_redis_connection

from blog.forms import CommentForm
from blog.models import Post, Category

redis_connection = get_redis_connection('default')


def post_list(request):
    category_slug = request.GET.get('c', None)
    posts = Post.objects.filter(published=True)
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    paginator = Paginator(posts, 10)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        posts = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'blog/post_ajax.html', {'posts': posts})
    return render(request, 'blog/home.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    likes = post.likes
    liked = request.session.get(f'like-{post.id}', False)
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(reverse('post_detail', args=[post.slug]))
    else:
        comment_form = CommentForm()
    return render(request, 'blog/post_detail.html', {'post': post, 'comment_form': comment_form, 'likes': likes,
                                                     'liked': liked})


@require_POST
def post_like(request):
    post_id = int(request.POST.get('post_id', 0))
    post = get_object_or_404(Post, id=post_id)
    redis_connection.incr(f'post:{post_id}:views')
    if request.session.get(f'like-{post_id}', False):
        post.likes = F('likes') - 1
        request.session[f'like-{post_id}'] = False
    else:
        post.likes = F('likes') + 1
        request.session[f'like-{post_id}'] = True
    post.save()
    post.refresh_from_db()
    likes = post.likes
    return HttpResponse(likes)


def search(request):
    query = request.GET.get('query')
    posts = Post.objects.annotate(
        similarity=TrigramSimilarity('title', query),
    ).filter(similarity__gt=0.3, published=True).order_by('-similarity')
    return render(request, 'blog/search.html', {'query': query, 'posts': posts})


class AboutMeView(TemplateView):
    template_name = 'about_me.html'


class ContactInfoView(TemplateView):
    template_name = 'contact_info.html'


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'

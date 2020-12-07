import redis
from django.conf import settings
from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.generic import TemplateView

from blog.forms import CommentForm
from blog.models import Post


r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)


def post_list(request):
    posts = Post.objects.filter(published=True)
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
    likes = int(r.get(f'post:{post.id}:likes')or 0)
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
    post_id = request.POST.get('post_id', None)
    if request.session.get(f'like-{post_id}', False):
        total_likes = r.decr(f'post:{post_id}:likes')
        request.session[f'like-{post_id}'] = False
    else:
        total_likes = r.incr(f'post:{post_id}:likes')
        request.session[f'like-{post_id}'] = True
    return HttpResponse(str(total_likes))


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

from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class BlogTest(TestCase):
    @staticmethod
    def create_post(title='Title', slug='slug', content='Content', is_published=True, category=None):
        return Post.objects.create(title=title, slug=slug, content=content, is_published=is_published,
                                   category=category)

    @staticmethod
    def create_n_posts(n):
        for i in range(n):
            BlogTest.create_post(title=str(i), slug=str(i))

    def get_ajax_request(self, url):
        return self.client.get(url, **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

    def get_post_detail_with_given_slug(self, slug):
        return self.client.get(reverse('blog:post_detail', args=[slug]))

    def comment_post_with_given_slug(self, slug, comment_author, comment_content):
        data = {'author': comment_author, 'content': comment_content}
        return self.client.post(reverse('blog:post_detail', args=[slug]), data=data, follow=True)

    def like_post(self, post_id):
        return self.client.post(reverse('blog:post_like'), data={'post_id': post_id},
                                **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})

    def set_post_liked_session_variable(self, post_id, value):
        session = self.client.session
        session[f'like-{post_id}'] = value
        session.save()

    @staticmethod
    def set_post_likes_to_n(post, n):
        post.likes = n
        post.save()

from django.template import loader
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Category


def create_post(title='Title', slug='slug', content='Content', published=True, category=None):
    return Post.objects.create(title=title, slug=slug, content=content, published=published, category=category)


def create_n_posts(n):
    for i in range(n):
        create_post(title=str(i), slug=str(i))


class TestPostListView(TestCase):
    def test_view_when_no_posts_prints_there_are_no_posts(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'No posts yet.')

    def test_view_displays_only_published_post(self):
        create_post(title='Published post', slug='published-post')
        create_post(title='Unpublished post', slug='unpublished-post', published=False)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['posts'], ['<Post: Published post>'])

    # Paginator displays only 10 posts per page
    def test_pagination_when_first_page_displays_only_10_posts(self):
        create_n_posts(n=12)
        expected_post_context = ['<Post: 11>', '<Post: 10>', '<Post: 9>', '<Post: 8>', '<Post: 7>',
                                 '<Post: 6>', '<Post: 5>', '<Post: 4>', '<Post: 3>', '<Post: 2>']
        response = self.client.get(reverse('home'))
        self.assertQuerysetEqual(response.context['posts'], expected_post_context)

    def test_pagination_when_last_page_displays_only_rest_of_posts(self):
        create_n_posts(n=12)
        expected_post_context = ['<Post: 1>', '<Post: 0>']
        response = self.client.get(f'{reverse("home")}/?page=2')
        self.assertQuerysetEqual(response.context['posts'], expected_post_context)

    def test_pagination_when_page_is_not_int_return_first_page(self):
        create_n_posts(n=12)
        expected_post_context = ['<Post: 11>', '<Post: 10>', '<Post: 9>', '<Post: 8>', '<Post: 7>',
                                 '<Post: 6>', '<Post: 5>', '<Post: 4>', '<Post: 3>', '<Post: 2>']
        response = self.client.get(f'{reverse("home")}/?page=not-int')
        self.assertQuerysetEqual(response.context['posts'], expected_post_context)

    def test_pagination_when_page_number_is_bigger_than_number_of_all_pages_return_last_page(self):
        create_n_posts(n=12)
        expected_post_context = ['<Post: 1>', '<Post: 0>']
        response = self.client.get(f'{reverse("home")}/?page=3')
        self.assertQuerysetEqual(response.context['posts'], expected_post_context)

    def test_view_when_category_is_not_given_displays_all_posts(self):
        category1 = Category.objects.create(name='Category1', slug='c1')
        category2 = Category.objects.create(name='Category2', slug='c2')
        create_post(title='Category 1 post', slug='c1', category=category1)
        create_post(title='Category 2 post', slug='c2', category=category2)
        response = self.client.get(reverse("home"))
        self.assertQuerysetEqual(response.context['posts'], ['<Post: Category 2 post>', '<Post: Category 1 post>'])

    def test_view_when_category_is_given_displays_posts_in_given_category(self):
        category1 = Category.objects.create(name='Category1', slug='c1')
        category2 = Category.objects.create(name='Category2', slug='c2')
        create_post(title='Category 1 post', slug='c1', category=category1)
        create_post(title='Category 2 post', slug='c2', category=category2)
        response = self.client.get(f'{reverse("home")}/?c=c1')
        self.assertQuerysetEqual(response.context['posts'], ['<Post: Category 1 post>'])

    def test_view_when_request_is_ajax_return_posts_html(self):
        create_n_posts(n=12)
        template = loader.get_template('blog/post_ajax.html')
        context = {
            'posts': Post.objects.all()[:10]
        }
        response = self.client.get(f'{reverse("home")}/?page=1', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, bytes(template.render(context), encoding='utf-8'))

    def test_view_when_request_is_ajax_and_page_number_is_bigger_than_number_of_all_pages_return_empty_bytes(self):
        create_n_posts(n=12)
        response = self.client.get(f'{reverse("home")}/?page=3', **{'HTTP_X_REQUESTED_WITH': 'XMLHttpRequest'})
        self.assertEqual(response.content, b'')


class TestPostDetailView(TestCase):
    def get_post_detail_with_given_slug(self, slug):
        return self.client.get(reverse('post_detail', args=[slug]))

    def comment_post_with_given_slug(self, slug, comment_author, comment_content):
        data = {'author': comment_author, 'content': comment_content}
        return self.client.post(reverse('post_detail', args=[slug]), data=data, follow=True)

    def test_view_when_proper_slug_is_given_returns_site(self):
        create_post(slug='slug')
        response = self.get_post_detail_with_given_slug('slug')
        self.assertEqual(response.status_code, 200)

    def test_view_raises_404_when_post_with_given_slug_does_not_exist(self):
        response = self.get_post_detail_with_given_slug(slug='slug_of_post_that_does_not_exist')
        self.assertEqual(response.status_code, 404)

    def test_create_comment_with_correct_data(self):
        create_post(slug='slug')
        author = 'CommentAuthor'
        content = 'CommentContent'
        response = self.comment_post_with_given_slug(slug='slug', comment_author=author, comment_content=content)
        self.assertContains(response, 'CommentAuthor')
        self.assertContains(response, 'CommentContent')

    def test_form_error_when_create_comment_with_incorrect_data(self):
        create_post(slug='slug')
        author = 'CommentAuthor'
        content = 'a\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na'
        response = self.comment_post_with_given_slug(slug='slug', comment_author=author, comment_content=content)
        self.assertContains(response, 'To many line breaks!')

    def test_when_site_is_visited_views_counter_is_incremented(self):
        pass


class TestPostLikeView(TestCase):
    def like_post(self, post_id):
        return self.client.post(reverse('post_like'), data={'post_id': post_id})

    def set_post_liked_session_variable(self, post_id, value):
        session = self.client.session
        session[f'like-{post_id}'] = value
        session.save()

    def get_post_liked_session_variable(self, post_id):
        return self.client.session[f'like-{post_id}']

    def test_when_post_is_unliked_by_user_increment_likes(self):
        post = create_post()
        response = self.like_post(post_id=post.id)
        self.assertEqual(response.content, b'1')

    def test_when_post_is_unliked_by_user_post_likes_session_variable_is_set_to_False(self):
        post = create_post()
        self.like_post(post_id=post.id)
        is_liked = self.get_post_liked_session_variable(post.id)
        self.assertEqual(is_liked, True)

    def test_when_post_is_liked_by_user_decrement_likes(self):
        post = create_post()
        post.likes = 1
        post.save()
        self.set_post_liked_session_variable(post_id=post.id, value=True)
        response = self.like_post(post.id)
        self.assertEqual(response.content, b'0')

    def test_when_post_is_liked_by_user_post_likes_session_variable_is_set_to_False(self):
        post = create_post()
        post.likes = 1
        post.save()
        self.set_post_liked_session_variable(post_id=post.id, value=True)
        self.like_post(post_id=post.id)
        is_liked = self.get_post_liked_session_variable(post.id)
        self.assertEqual(is_liked, False)


class TestSearchView(TestCase):
    pass

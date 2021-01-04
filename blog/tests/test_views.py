from django.template import loader
from django.test import TestCase
from django.urls import reverse

from blog.models import Post, Category
from blog.tests.utils import BlogTest


class TestPostListView(BlogTest):
    def test_when_there_are_no_posts_should_display_appropriate_message(self):
        response = self.get_post_list()
        self.assertContains(response, 'There are no posts yet')

    def test_display_only_published_post(self):
        self.create_post(title='Published post', slug='published-post')
        self.create_post(title='Unpublished post', slug='unpublished-post', is_published=False)
        response = self.get_post_list()
        self.assertQuerysetEqual(response.context['posts'], ['<Post: Published post>'])

    # Paginator displays only 10 posts per page
    def test_when_first_page_is_given_should_display_only_10_posts(self):
        self.create_n_posts(n=12)
        expected_context = ['<Post: 11>', '<Post: 10>', '<Post: 9>', '<Post: 8>', '<Post: 7>',
                            '<Post: 6>', '<Post: 5>', '<Post: 4>', '<Post: 3>', '<Post: 2>']
        response = self.get_post_list()
        self.assertQuerysetEqual(response.context['posts'], expected_context)

    def test_when_last_page_is_given_should_display_only_rest_of_posts(self):
        self.create_n_posts(n=12)
        expected_context = ['<Post: 1>', '<Post: 0>']
        response = self.get_post_list(page=2)
        self.assertQuerysetEqual(response.context['posts'], expected_context)

    def test_when_page_is_not_int_should_return_first_page(self):
        self.create_n_posts(n=12)
        expected_context = ['<Post: 11>', '<Post: 10>', '<Post: 9>', '<Post: 8>', '<Post: 7>',
                            '<Post: 6>', '<Post: 5>', '<Post: 4>', '<Post: 3>', '<Post: 2>']
        response = self.get_post_list(page='not-int')
        self.assertQuerysetEqual(response.context['posts'], expected_context)

    def test_when_given_page_number_is_bigger_than_number_of_all_pages_should_return_last_page(self):
        self.create_n_posts(n=12)
        expected_context = ['<Post: 1>', '<Post: 0>']
        response = self.get_post_list(page=3)
        self.assertQuerysetEqual(response.context['posts'], expected_context)

    def test_when_category_is_not_given_should_display_all_posts(self):
        category1 = Category.objects.create(name='Category1', slug='c1')
        category2 = Category.objects.create(name='Category2', slug='c2')
        self.create_post(title='Category 1 post', slug='c1', category=category1)
        self.create_post(title='Category 2 post', slug='c2', category=category2)
        expected_context = ['<Post: Category 2 post>', '<Post: Category 1 post>']
        response = self.get_post_list()
        self.assertQuerysetEqual(response.context['posts'], expected_context)

    def test_should_display_posts_in_given_category(self):
        category1 = Category.objects.create(name='Category1', slug='c1')
        category2 = Category.objects.create(name='Category2', slug='c2')
        self.create_post(title='Category 1 post', slug='c1', category=category1)
        self.create_post(title='Category 2 post', slug='c2', category=category2)
        expected_context = ['<Post: Category 1 post>']
        response = self.get_post_list(category='c1')
        self.assertQuerysetEqual(response.context['posts'], expected_context)

    def test_when_request_is_ajax_should_return_posts_html(self):
        self.create_n_posts(n=12)
        template = loader.get_template('blog/post_ajax.html')
        context = {
            'posts': Post.objects.all()[:10]
        }
        response = self.get_ajax_request(url=f'{reverse("blog:post_list")}/?page=1')
        self.assertEqual(response.content, bytes(template.render(context), encoding='utf-8'))

    def test_when_request_is_ajax_and_page_number_is_bigger_than_number_of_all_pages_should_return_empty_bytes(self):
        self.create_n_posts(n=12)
        response = self.get_ajax_request(url=f'{reverse("blog:post_list")}/?page=3')
        self.assertEqual(response.content, b'')


class TestPostDetailView(BlogTest):
    def test_when_proper_slug_is_given_should_return_page(self):
        self.create_post(slug='slug')
        response = self.get_post_detail_with_given_slug(slug='slug')
        self.assertEqual(response.status_code, 200)

    def test_when_post_with_given_slug_does_not_exist_should_return_404(self):
        response = self.get_post_detail_with_given_slug(slug='slug_of_post_that_does_not_exist')
        self.assertEqual(response.status_code, 404)

    def test_create_comment_with_correct_data(self):
        self.create_post(slug='slug')
        author = 'CommentAuthor'
        content = 'CommentContent'
        response = self.comment_post_with_given_slug(slug='slug', comment_author=author,
                                                     comment_content=content)
        self.assertContains(response, 'CommentAuthor')
        self.assertContains(response, 'CommentContent')

    def test_when_comment_data_is_incorrect_should_display_error(self):
        self.create_post(slug='slug')
        author = 'CommentAuthor'
        content = 'a\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na'
        response = self.comment_post_with_given_slug(slug='slug', comment_author=author,
                                                     comment_content=content)
        self.assertContains(response, 'To many line breaks!')

    # def test_when_site_is_visited_should_increment_views_counter(self):
    #     slug = 'test'
    #     post = self.create_post(slug=slug)
    #     views = post.number_of_views
    #     self.get_post_detail_with_given_slug(slug=slug)
    #     self.assertEqual(post.number_of_views, views+1)


class TestPostLikeView(BlogTest):
    def test_when_post_is_not_liked_should_increment_likes(self):
        post = self.create_post()
        response = self.like_post(post_id=post.id)
        post.refresh_from_db()
        self.assertEqual(response.content, b'1')
        self.assertEqual(post.likes, 1)

    def test_when_post_is_not_liked_should_set_session_variable_to_True(self):
        post = self.create_post()
        self.like_post(post_id=post.id)
        self.assertEqual(post.is_liked(self.client), True)

    def test_when_post_is_liked_should_decrement_likes(self):
        post = self.create_post()
        post.likes = 1
        post.save()
        self.set_post_liked_session_variable(post_id=post.id, value=True)
        response = self.like_post(post_id=post.id)
        self.assertEqual(response.content, b'0')

    def test_when_post_is_liked_should_set_session_variable_to_False(self):
        post = self.create_post()
        post.likes = 1
        post.save()
        self.set_post_liked_session_variable(post_id=post.id, value=True)
        self.like_post(post_id=post.id)
        self.assertEqual(post.is_liked(self.client), False)

    def test_when_post_with_given_id_does_not_exist_should_return_404(self):
        response = self.like_post(post_id='9999999999')
        self.assertEqual(response.status_code, 404)

    def test_when_given_id_is_not_int_should_return_404(self):
        response = self.like_post(post_id=['test'])
        self.assertEqual(response.status_code, 404)

        response = self.like_post(post_id='test')
        self.assertEqual(response.status_code, 404)


# class TestSearchView(BlogTest):
#     def test_when_there_are_no_similar_posts_should_display_appropriate_message(self):
#         response = self.client.get(reverse('blog:search'), args=['title'])
#         self.assertContains(response, 'There are no posts matching the query.')
#
#     def test_should_display_only_similar_posts(self):
#         self.create_post(title='Test 1', slug='slug-1')
#         self.create_post(title='Test 2', slug='slug-2')
#         self.create_post(title='Not similar', slug='slug-3')
#         expected_context = ['<Post: Test 2>', '<Post: Test 1>']
#         response = self.client.get(reverse('blog:search', args=['Test']))
#         self.assertQuerysetEqual(response.context['posts'], expected_context)


class TestCategoryListView(TestCase):
    def setUp(self):
        Category.objects.create(name='Category1', slug='category1')
        Category.objects.create(name='Category2', slug='category2')

    def test_displays_categories(self):
        response = self.client.get(reverse('blog:categories'))
        expected_context = ['<Category: Category1>', '<Category: Category2>']
        self.assertQuerysetEqual(response.context['categories'], expected_context, ordered=False)


class TestTopPostsView(BlogTest):
    def test_when_there_are_no_posts_should_display_appropriate_message(self):
        response = self.client.get(reverse('blog:top_posts'))
        self.assertContains(response, 'There are no posts yet.')

    def test_should_display_top_5_posts_by_views(self):
        posts = [self.create_post(title=str(i), slug=str(i)) for i in range(10)]
        for i, post in enumerate(posts[:5]):
            post._views_counter._set_number_of_views(i)
        expected_context = ['<Post: 9>', '<Post: 8>', '<Post: 7>', '<Post: 6>', '<Post: 5>']
        response = self.client.get(reverse('blog:top_posts'))
        self.assertQuerysetEqual(response.context['top_viewed_posts'], expected_context)

    def test_should_display_top_5_posts_by_likes(self):
        posts = [self.create_post(title=char, slug=char) for char in 'abcdef']
        for i, post in enumerate(posts[:-1]):
            post.likes = i + 1
            post.save()
        expected_context = ['<Post: e>', '<Post: d>', '<Post: c>', '<Post: b>', '<Post: a>']
        response = self.client.get(reverse('blog:top_posts'))
        self.assertQuerysetEqual(response.context['top_liked_posts'], expected_context)

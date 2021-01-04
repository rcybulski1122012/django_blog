from unittest.mock import MagicMock

from django.test import SimpleTestCase

from blog.views_counter import PostViewsCounter


class TestViewsCounter(SimpleTestCase):
    def setUp(self):
        self.post = self.create_fake_post()

    @staticmethod
    def create_fake_post():
        fake_post = MagicMock()
        fake_post.id.return_value = 12345
        return fake_post

    def test_get_number_of_views_when_value_is_set_should_return_it(self):
        PostViewsCounter(self.post)._set_number_of_views(5)
        number_of_views = PostViewsCounter(self.post).get_number_of_views()
        self.assertEqual(number_of_views, 5)

    def test_get_number_of_views_when_value_is_not_set_should_return_0(self):
        number_of_views = PostViewsCounter(self.post).get_number_of_views()
        self.assertEqual(number_of_views, 0)

    def test_increment_views_counter(self):
        views_counter = PostViewsCounter(self.post)
        views_counter._set_number_of_views(5)
        views_counter.increment()
        number_of_views_after = views_counter.get_number_of_views()
        self.assertEqual(number_of_views_after, 6)

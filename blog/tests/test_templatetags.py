from django.http import HttpRequest
from django.test import SimpleTestCase

from blog.templatetags.blog_tags import is_navbar_item_active, get_category, get_number_of_current_page


class TestIsNavbarItemActiveTag(SimpleTestCase):
    def setUp(self):
        # testing with post_list view whose url is '/'
        self.request = HttpRequest()
        self.request.path = '/'

    def test_when_name_is_matching_request_path_should_return_active(self):
        self.assertEqual(is_navbar_item_active(self.request, 'blog:post_list'), 'active')

    def test_when_name_is_not_matching_request_path_should_return_empty_str(self):
        self.assertEqual(is_navbar_item_active(self.request, 'blog:search'), '')


class TestGetCategoryTag(SimpleTestCase):
    def test_when_category_in_GET_should_return_category(self):
        request = HttpRequest()
        request.GET['c'] = 'category'
        self.assertEqual(get_category(request), 'category')

    def test_when_category_not_in_GET_should_return_empty_str(self):
        request = HttpRequest()
        self.assertEqual(get_category(request), '')


class TestGetPageTag(SimpleTestCase):
    def test_when_page_in_GET_should_return_page(self):
        request = HttpRequest()
        request.GET['page'] = 100
        self.assertEqual(get_number_of_current_page(request), 100)

    def test_when_page_not_in_GET_should_return_1(self):
        request = HttpRequest()
        self.assertEqual(get_number_of_current_page(request), 1)

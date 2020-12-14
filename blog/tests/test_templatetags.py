from django.http import HttpRequest
from django.test import TestCase

from blog.templatetags.blog_tags import is_navbar_item_active


class TestBlogTemplateTags(TestCase):
    def setUp(self):
        # testing with 'home' view whose url is '/'
        self.request = HttpRequest()
        self.request.path = '/'

    def test_when_name_is_matching_request_path_is_active_tag_returns_active(self):
        self.assertEqual(is_navbar_item_active(self.request, 'home'), 'active')

    def test_when_name_in_not_matching_request_path_is_active_tag_returns_empty_str(self):
        self.assertEqual(is_navbar_item_active(self.request, 'search'), '')

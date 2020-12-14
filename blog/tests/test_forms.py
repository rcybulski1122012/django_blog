from django.test import SimpleTestCase

from blog.forms import CommentForm


class TestCommentForm(SimpleTestCase):
    def test_valid_form(self):
        data = {'author': 'author', 'content': 'content'}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_when_comment_body_contain_too_many_line_breaks(self):
        data = {'author': 'author', 'content': 'a\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na'}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_when_data_is_empty(self):
        data = {'author': '', 'comment': ''}
        form = CommentForm(data=data)
        self.assertFalse((form.is_valid()))

from blog.forms import CommentForm
from blog.tests.utils import BlogTest


class TestCommentForm(BlogTest):
    def test_valid_form(self):
        data = {'author': 'author', 'content': 'content'}
        form = CommentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_when_comment_body_contain_too_many_line_breaks_form_should_be_invalid(self):
        data = {'author': 'author', 'content': 'a\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na\na'}
        form = CommentForm(data=data)
        self.assertFalse(form.is_valid())

    def test_when_data_is_empty_form_should_be_invalid(self):
        data = {'author': '', 'comment': ''}
        form = CommentForm(data=data)
        self.assertFalse((form.is_valid()))

    def test_save_with_post(self):
        post = self.create_post()
        data = {'author': 'author', 'content': 'content'}
        form = CommentForm(data=data)
        comment = form.save_with_post(post)
        self.assertEqual(list(post.comments.all())[-1], comment)

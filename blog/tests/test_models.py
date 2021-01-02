from blog.tests.utils import BlogTest


class TestPostModel(BlogTest):
    def setUp(self):
        self.post = self.create_post()

    def test_number_of_views(self):
        self.post._views_counter._set_number_of_views(5)
        self.assertEqual(self.post.number_of_views, 5)

    def test_increment_views_counter(self):
        self.post._views_counter._set_number_of_views(5)
        self.post.increment_views_counter()
        self.assertEqual(self.post.number_of_views, 6)

    def test_like_when_post_is_not_liked_should_increment_likes(self):
        self.set_post_likes_to_n(self.post, 5)
        self.post.like(self.client)
        self.assertEqual(self.post.likes, 6)

    def test_like_when_post_is_liked_should_decrement_likes(self):
        self.set_post_likes_to_n(self.post, 5)
        self.set_post_liked_session_variable(post_id=self.post.id, value=True)
        self.post.like(self.client)
        self.assertEqual(self.post.likes, 4)

    # def test_like_when_post_is_liked_should_set_session_variable_to_False(self):
    #     self.set_post_likes_to_n(self.post, 5)
    #     self.set_post_liked_session_variable(post_id=self.post.id, value=True)
    #     self.post.like(self.client)
    #     self.assertFalse(self.post.is_liked(self.client))
    #
    # def test_like_when_post_is_not_liked_should_set_session_variable_to_True(self):
    #     self.set_post_likes_to_n(self.post, 5)
    #     self.set_post_liked_session_variable(post_id=self.post.id, value=False)
    #     self.post.like(self.client)
    #     self.assertTrue(self.post.is_liked(self.client))

    def test_is_liked(self):
        self.set_post_liked_session_variable(post_id=self.post.id, value=True)
        self.assertTrue(self.post.is_liked(self.client))

        self.set_post_liked_session_variable(post_id=self.post.id, value=False)
        self.assertFalse(self.post.is_liked(self.client))

from django_redis import get_redis_connection

redis_connection = get_redis_connection('default')


class PostViewsCounter:
    def __init__(self, post):
        self._key = f'post:{post.id}:views'

    def get_number_of_views(self):
        return int(redis_connection.get(self._key) or 0)

    def increment(self):
        redis_connection.incr(self._key)

    def _set_number_of_views(self, value):
        redis_connection.set(self._key, value)

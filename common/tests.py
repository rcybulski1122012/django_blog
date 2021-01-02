from django.http import HttpResponse, HttpRequest, HttpResponseBadRequest
from django.test import SimpleTestCase

from common.decorators import ajax_required


class TestAjaxRequiredDecorator(SimpleTestCase):
    def test_decorated_view_when_request_is_not_ajax_returns_bad_request_response(self):
        request = HttpRequest()
        response = fake_view(request)
        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_decorated_view_when_request_is_ajax_returns_proper_value(self):
        request = HttpRequest()
        request.META['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = fake_view(request)
        self.assertEqual(response.content, b'OK')


@ajax_required
def fake_view(request):
    return HttpResponse('OK')

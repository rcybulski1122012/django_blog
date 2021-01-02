from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(name='active')
def is_navbar_item_active(request, name):
    return 'active' if name == resolve(request.path).view_name else ''


@register.simple_tag(name='category')
def get_category(request):
    return request.GET.get('c', '')


@register.simple_tag(name='page')
def get_number_of_current_page(request):
    return request.GET.get('page', 1)

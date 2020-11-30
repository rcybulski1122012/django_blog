from django import template
from django.urls import resolve

register = template.Library()


@register.simple_tag(name='active')
def is_navbar_item_active(request, name):
    return 'active' if name == resolve(request.path).view_name else ''

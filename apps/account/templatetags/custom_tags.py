from django.conf import settings
from django.urls import reverse
from django import template

register = template.Library()


@register.simple_tag
def url_absolute(page):
    return settings.DOMAIN_URL + reverse(page)



@register.filter('float_str')
def float_str(value):
    float = str(value)
    return float.replace(',', '.')
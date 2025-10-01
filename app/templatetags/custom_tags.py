from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def path_host_url(viewname, *args, **kwargs):
    # You could make this dynamic with an env var!
    base = "/app"
    url = reverse(viewname, args=args, kwargs=kwargs)
    return f"{base}{url}"

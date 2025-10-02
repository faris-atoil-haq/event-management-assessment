from django import template
from django.urls import reverse

register = template.Library()


@register.simple_tag
def path_host_url(viewname, *args, **kwargs):
    # You could make this dynamic with an env var!
    base = "/app"
    url = reverse(viewname, args=args, kwargs=kwargs)
    return f"{base}{url}"

@register.filter
def get_initial_name(user):
    if user.first_name and user.last_name:
        return f"{user.first_name[0]}{user.last_name[0]}".upper()
    elif user.first_name:
        return f"{user.first_name[:2]}".upper()
    elif user.last_name:
        return f"{user.last_name[:2]}".upper()
    else:
        if user.email:
            return f"{user.email[:2]}".upper()
        return "NA"
    

@register.filter
def to_string(date):
    if date:
        return str(date)[0:10]
    return ""

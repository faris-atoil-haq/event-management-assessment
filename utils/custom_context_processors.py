from django.conf import settings

def custom_context(request):
    context = {
        'PROD': settings.PROD,
        'STAGING': settings.STAGING,
        'DEBUG': settings.DEBUG,
    }
    
    homepage_url = f"{request.__dict__.get('META').get('HTTP_HOST')}"
    homepage_url_final = homepage_url
    
    if len(homepage_url.split('.')) > 1:
        homepage_url_merge = ".".join(homepage_url.split('.')[1:])
        homepage_url_final = homepage_url_merge.split('/')[0]
    context['homepage_url'] = f"http://{homepage_url_final}"
    return context

    
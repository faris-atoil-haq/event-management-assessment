from django.conf import settings
from app.constant.model_constant import *

def custom_context(request):
    context = {
        'STATUS_CHOICE': STATUS_CHOICES,
        'ROLE_CHOICE': ROLE_CHOICES,
        'PROD': settings.PROD,
        'STAGING': settings.STAGING,
        'DEBUG': settings.DEBUG,
        'CONSTANT': CONSTANT_LIST,
    }
    return context

    
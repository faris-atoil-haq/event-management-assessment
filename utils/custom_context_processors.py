from django.conf import settings
from app.models import Event, Verification
from app.constant.model_constant import CONSTANT_LIST
def custom_context(request):
    context = {
        'STATUS_CHOICE': Event.STATUS_CHOICES,
        'ROLE_CHOICE': Verification.ROLE_CHOICES,
        'PROD': settings.PROD,
        'STAGING': settings.STAGING,
        'DEBUG': settings.DEBUG,
        'CONSTANT': CONSTANT_LIST,
    }
    return context

    
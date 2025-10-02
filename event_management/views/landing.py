from django.shortcuts import redirect, render
from django.urls import reverse
import logging as logging

logger = logging.getLogger(__name__)


def landing_page(request, public=True):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return render(request, 'main/templates/landing_page.html', {'public': public})

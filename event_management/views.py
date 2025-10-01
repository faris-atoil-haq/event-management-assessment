from django.shortcuts import redirect, render
from django_hosts.resolvers import reverse
import logging as logging

logger = logging.getLogger(__name__)


def index(request, public=True):
    if request.user.is_authenticated:
        return redirect(reverse('dashboard'))
    return render(request, 'main/templates/index.html', {'public': public})

def handle_400(request, exception):
    return render(request, 'error_handler.html', {'error_code': '400'}, status=400)

def handle_404(request, exception):
    return render(request, 'error_handler.html', {'error_code': '404'}, status=404)

def handle_500(request):
    return render(request, 'error_handler.html', {'error_code': '500'}, status=500)

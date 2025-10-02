from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from app.models import Event
import logging as logging

logger = logging.getLogger(__name__)


@login_required
def dashboard(request, content_type='dashboard'):
    return render(request, 'app/templates/app-dashboard.html', {content_type: True})

@login_required
def create_and_manage_events(request, id=None):
    user = request.user
    event = {'id': ''}
    if id:
        event = Event.objects.filter(id=id).first()
        
    if request.POST:
        if 'delete-event' in request.POST:
            event.delete()
        else:
            if not id:
                event = Event.objects.create(user=user)
            event.title = request.POST.get('name')
            event.date_start = request.POST.get('date_start')
            event.date_end = request.POST.get('date_end')
            event.status = request.POST.get('status')
            event.description = request.POST.get('description')
            event.save()
        
        return redirect(reverse('events'))
    return render(request, 'app/templates/manage-events-drawer.html', {'events': True, 'event': event})

@login_required
def events_table(request):
    user = request.user
    events = Event.objects.filter(user=user).order_by('-created_at')
    return render(request, 'app/templates/events-table.html', {'events': events})

@login_required
def dashboard_content(request):
    user = request.user
    events = Event.objects.filter(user=user).order_by('date_start')
    return render(request, 'app/templates/app-dashboard-content.html', {'dashboard': True, 'events': events})


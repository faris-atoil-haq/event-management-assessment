from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.urls import reverse
from app.models import Event, Track
import logging as logging
from utils.check_newly_object import auto_refresh_db
from app.constant.model_constant import MANAGER_ROLE, MEMBER_ROLE

logger = logging.getLogger(__name__)


@login_required
def dashboard(request, content_type='dashboard'):
    # Clean up newly created events
    res = auto_refresh_db(user=request.user)
    print(f"Cleanup newly created events: {res}")
    logger.info(f"Cleanup newly created events: {res}")

    return render(request, 'app/templates/app-dashboard.html', {content_type: True})

@login_required
def create_and_manage_events(request, id=None):
    user = request.user
    if id:
        event = Event.objects.filter(id=id).first()
    else:
        event = Event.objects.create(user=user)
        
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
            
            manage_track(request)
        
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
    role = user.verification.role
    if role == MEMBER_ROLE:
        events = Event.objects.all().order_by('date_start')
    elif role == MANAGER_ROLE:
        events = Event.objects.filter(user=user).order_by('date_start')
    events = events.filter(status='published')
    return render(request, 'app/templates/app-dashboard-content.html', {'dashboard': True, 'events': events})

@login_required
def manage_track(request):
    if request.POST:
        if 'delete_track' in request.POST and 'track_id' in request.POST:
            track_id = request.POST.get('track_id')
            Track.objects.filter(id=track_id).delete()
            return HttpResponse("")

        print(f"Saving Tracks: {request.POST}")
        track_ids = request.POST.getlist('track_id')
        names = request.POST.getlist('track_name')
        descriptions = request.POST.getlist('track_description', '')
        
        # Use .update() for bulk updating existing tracks
        existing_tracks = Track.objects.filter(id__in=[tid for tid in track_ids if tid]).order_by('id')
        for order, track, name, description in zip(range(len(existing_tracks)), existing_tracks, names, descriptions):
            track.order = order + 1
            track.name = name
            track.description = description
        Track.objects.bulk_update(existing_tracks, ['order','name', 'description'])
    else:
        event_id = request.GET.get('event_id')
        track_id = request.GET.get('track_id',None)
        event = Event.objects.filter(id=event_id).first() if event_id else None 
        if track_id:
            track = Track.objects.filter(id=track_id).first()
        else:
            track = Track.objects.create(event=event) if event else None
        track_count = Track.objects.filter(
            event=event).count() if event else 0
        return render(request, 'app/templates/manage-tracks.html', {'number': track_count, 'track': track if track else None, 'event': event})
    return HttpResponse(200)


def show_event_detail(request, event_id):
    event = Event.objects.filter(id=event_id).first()
    if not event:
        return HttpResponse("Event not found", status=404)
    return render(request, 'app/templates/attendee-event-detail.html', {'event': event})

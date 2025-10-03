from datetime import datetime
from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from app.models import Event, Session, Track


@login_required
def manage_track_session(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    sessions = track.sessions.all().order_by('start_time')
    return render(request, 'app/templates/manage-session.html', {
        'track': track,
        'sessions': sessions
    })

@login_required
def create_and_manage_session(request):
    if request.method == 'POST':
        track = Track.objects.get(id=request.POST['track_id'])
        if 'session_id' in request.POST:
            session = get_object_or_404(Session, id=request.POST['session_id'])
        else:
            session = Session(track=track)
        if request.POST.get('delete-session'):
            session.delete()
            return redirect(reverse('manage_track_session', args=[track.id]))
        session.title = request.POST['session_title']
        session.description = request.POST['session_description']
        session.start_time = request.POST['session_start_time']
        session.end_time = request.POST['session_end_time']
        session.speaker = request.POST['session_speaker']

        session.start_time = datetime.strptime(session.start_time, "%H:%M")
        session.end_time = datetime.strptime(session.end_time, "%H:%M")
        try:
            session.save()
            messages.success(request, 'Session updated successfully!')
        except ValidationError as e:
            print(f"Error: {e.message}")
            messages.error(request, f'Error: {e.message}')
        return redirect(reverse('manage_track_session', args=[track.id]))

@login_required
def session_list(request, track_id):
    track = get_object_or_404(Track, id=track_id, user=request.user)
    sessions = track.sessions.all().order_by('start_time')
    return render(request, 'app/templates/session_list.html', {
        'track': track,
        'sessions': sessions
    })
    
@login_required
def load_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    track = session.track
    sessions = track.sessions.all().exclude(id=session.id).order_by('start_time')
    return render(request, 'app/templates/manage-session.html', {
        'session': session,
        'sessions': sessions
    })
    
@login_required
def manage_tracks(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)

    if request.method == 'POST':
        track = Track(
            event=event,
            name=request.POST['name'],
            description=request.POST['description'],
        )
        track.save()
        messages.success(request, 'Track created successfully!')

    tracks = event.tracks.all()
    return render(request, 'app/templates/manage-tracks.html', {
        'event': event,
        'tracks': tracks
    })

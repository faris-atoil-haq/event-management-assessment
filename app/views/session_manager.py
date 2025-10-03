from django.core.exceptions import ValidationError
from django.http.response import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Event, Session, Track


@login_required
def create_session(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)

    if request.method == 'POST':
        session = Session(
            event=event,
            title=request.POST['title'],
            description=request.POST['description'],
            start_time=request.POST['start_time'],
            end_time=request.POST['end_time'],
            speaker=request.POST['speaker'],
            capacity=request.POST['capacity']
        )

        if request.POST.get('track_id'):
            session.track_id = request.POST['track_id']

        try:
            session.full_clean()
            session.save()
            messages.success(request, 'Session created successfully!')
            return redirect('event_detail', event_id=event.id)
        except ValidationError as e:
            messages.error(request, f'Error: {e.message}')

    tracks = event.tracks.all()
    return render(request, 'app/templates/create-session.html', {
        'event': event,
        'tracks': tracks
    })
    
@login_required
def manage_track_session(request, track_id):
    track = get_object_or_404(Track, id=track_id)
    sessions = track.sessions.all().order_by('start_time')
    return render(request, 'app/templates/manage-session.html', {
        'track': track,
        'sessions': sessions
    })

@login_required
def manage_session(request, session_id):
    session = get_object_or_404(Session, id=session_id, event__user=request.user)
    if request.method == 'POST':
        if request.POST.get('delete-session'):
            session.delete()
            return HttpResponse('Session deleted successfully!')
        session.title = request.POST['title']
        session.description = request.POST['description']
        session.start_time = request.POST['start_time']
        session.end_time = request.POST['end_time']
        session.speaker = request.POST['speaker']

        try:
            session.full_clean()
            session.save()
            messages.success(request, 'Session updated successfully!')
            return HttpResponse('Session updated successfully!')
        except ValidationError as e:
            messages.error(request, f'Error: {e.message}')


@login_required
def session_list(request, track_id):
    track = get_object_or_404(Track, id=track_id, user=request.user)
    sessions = track.sessions.all().order_by('start_time')
    return render(request, 'app/templates/session_list.html', {
        'track': track,
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

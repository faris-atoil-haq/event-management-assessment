from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Event, Attendee


@login_required
def register_for_event(request, event_id):
    print(request.POST)
    event = get_object_or_404(Event, id=event_id)
    registered = False
    # Check event capacity
    if event.capacity and event.attendees.count() >= event.capacity:
        messages.error(request, 'Event was full!')
        return redirect('event_detail', event_id=event_id)

    try:
        attendee = Attendee.objects.create(
            user=request.user,
            event=event
        )
        messages.success(
            request, f'Successful registration for "{event.title}"!')
    except IntegrityError:
        registered = True
        messages.warning(request, 'You are already registered for this event!')
    if 'register_with_view' in request.POST:
        if registered:
            return redirect('cancel_registration', request,event_id)
        return redirect('dashboard')
    return redirect('event_detail', event_id=event_id)


@login_required
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        attendee = Attendee.objects.get(user=request.user, event=event)
        attendee.delete()
        messages.success(request, 'Successful cancellation of registration!')
    except Attendee.DoesNotExist:
        messages.error(request, 'You are not registered for this event!')
    if 'register_with_view' in request.POST:
        return redirect('dashboard')        
    return redirect('event_detail', event_id=event_id)


@login_required
def attendee_list(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    attendees = event.attendees.all().order_by('registration_date')
    return render(request, 'app/templates/attendee_list.html', {
        'event': event,
        'attendees': attendees
    })

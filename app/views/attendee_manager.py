from django.db.utils import IntegrityError
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from app.models import Event, Attendee


@login_required
def register_for_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)

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
            request, f'Anda berhasil mendaftar untuk event "{event.title}"!')
    except IntegrityError:
        messages.warning(request, 'Anda sudah terdaftar untuk event ini!')

    return redirect('event_detail', event_id=event_id)


@login_required
def cancel_registration(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        attendee = Attendee.objects.get(user=request.user, event=event)
        attendee.delete()
        messages.success(request, 'Pendaftaran berhasil dibatalkan!')
    except Attendee.DoesNotExist:
        messages.error(request, 'Anda tidak terdaftar untuk event ini!')

    return redirect('event_detail', event_id=event_id)


@login_required
def attendee_list(request, event_id):
    event = get_object_or_404(Event, id=event_id, user=request.user)
    attendees = event.attendees.all().order_by('registration_date')
    return render(request, 'app/templates/attendee_list.html', {
        'event': event,
        'attendees': attendees
    })

from app.models import Event, Track


def auto_refresh_db(user=None):
    """Get all newly created events with to delete unused Event objects."""
    queryset = Event.objects.all()
    if user:
        queryset = queryset.filter(user=user)

    newly_created = []
    for event in queryset:
        # Check with 1-second tolerance for microsecond differences
        time_diff = abs((event.updated_at - event.created_at).total_seconds())
        if time_diff < 1:
            newly_created.append(event.id)
    if newly_created:
        Event.objects.filter(id__in=newly_created).delete()

    queryset = Track.objects.filter(name__isnull=True, description__isnull=True)
    if user:
        queryset = queryset.filter(event__user=user)
    queryset.delete()
    
    return ''
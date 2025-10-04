import uuid
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User
from app.constant.model_constant import STATUS_CHOICES

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    order = models.CharField(max_length=256, null=True, blank=True)
    capacity = models.IntegerField(null=True, blank=True)
    venue = models.CharField(max_length=256, null=True, blank=True)
    venue_address = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # Registration settings
    registration_open = models.BooleanField(default=True)
    registration_deadline = models.DateTimeField(null=True, blank=True)
    
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='draft')

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return self.title or f"Event {self.id}"

    @property
    def is_registration_open(self):
        """Check if registration is still open"""
        if not self.registration_open:
            return False
        if self.registration_deadline and timezone.now() > self.registration_deadline:
            return False
        if self.capacity > 0 and self.attendees.count() >= self.capacity:
            return False
        return True

    @property
    def attendee_count(self):
        """Get current number of attendees"""
        return self.attendees.filter(status='registered').count()

    @property
    def available_spots(self):
        """Get remaining spots available"""
        if self.capacity == 0:
            return "Unlimited"
        return max(0, self.capacity - self.attendee_count)

    @property
    def is_full(self):
        """Check if event is at capacity"""
        if self.capacity == 0:
            return False
        return self.attendee_count >= self.capacity

    @property
    def is_newly_created(self):
        """Check if event has never been updated"""
        if not self.created_at or not self.updated_at:
            return True
        time_diff = abs((self.updated_at - self.created_at).total_seconds())
        return time_diff < 1
class Track(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False,
                            null=False)
    description = models.TextField(blank=True)
    event = models.ForeignKey(
        'Event', on_delete=models.CASCADE, related_name='tracks')
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.order} - {self.name}|{self.event.title}"

    @property
    def session_count(self):
        """Get number of sessions in this track"""
        return self.sessions.count()

    def get_sessions_by_day(self):
        """Group sessions by day"""
        from collections import defaultdict
        sessions_by_day = defaultdict(list)

        for session in self.sessions.all().order_by('start_time'):
            day = session.start_time.date()
            sessions_by_day[day].append(session)

        return dict(sessions_by_day)

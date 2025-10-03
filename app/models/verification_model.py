from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from .event_model import Event
from .session_model import Session
import uuid
class Verification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_query_name="verification"
    )
    verified = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    address = models.CharField(max_length=256, null=True, blank=True)
    code = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    ROLE_CHOICES = [
        ('member', 'Event Member'),
        ('manager', 'Event Manager')
    ]

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default='member')

    def __str__(self):
        return 'Verification for: ' + self.user.first_name


class Attendee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='attendees')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('registered', 'Terdaftar'),
        ('confirmed', 'Dikonfirmasi'),
        ('cancelled', 'Dibatalkan'),
    ], default='registered')

    class Meta:
        unique_together = ['user', 'event']  # Mencegah pendaftaran ganda

    def __str__(self):
        return f"{self.user.username} - {self.event.title}"


class SessionAttendee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    attendee = models.ForeignKey(Attendee, on_delete=models.CASCADE)
    session = models.ForeignKey(
        Session, on_delete=models.CASCADE, related_name='attendees')
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['attendee', 'session']

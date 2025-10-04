from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from .event_model import Event
import uuid
from app.constant.model_constant import (
    ROLE_CHOICES, 
    ATTENDEE_STATUS,
    MEMBER_ROLE,
    REGISTERED_ATTENDEE
)

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


    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=MEMBER_ROLE)

    def __str__(self):
        return 'Verification for: ' + self.user.first_name


class Attendee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user_attendees')
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, related_name='attendees')
    registration_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=ATTENDEE_STATUS, default=REGISTERED_ATTENDEE)

    class Meta:
        unique_together = ['user', 'event']  # Prevent duplicated registration
        
    def __str__(self):
        return f"{self.user.username} - {self.event.title}"
    
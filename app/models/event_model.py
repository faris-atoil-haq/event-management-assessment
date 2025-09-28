import uuid
from django.db import models
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.models import User


class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    order = models.CharField(max_length=256, null=True, blank=True)
    duration = models.CharField(max_length=256, null=True, blank=True)
    time_event = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    created_by = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)


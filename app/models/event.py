import uuid
from django.db import models
from django.utils import timezone
from datetime import datetime

class Event(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    date_start = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    order = models.CharField(max_length=256, null=True, blank=True)
    duration = models.CharField(max_length=256, null=True, blank=True)
    time_increment = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    schedule_days = models.TextField(null=True, blank=True)
    schedule_start_time = models.TextField(null=True, blank=True)
    schedule_end_time = models.TextField(null=True, blank=True)
    time_event = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    url = models.CharField(max_length=256, null=True, blank=True)
    created_by = models.CharField(max_length=256, null=True, blank=True)
    slug = models.CharField(max_length=256, null=True, blank=True)
    _id = models.TextField(null=True, blank=True)
    _id_add = models.TextField(null=True, blank=True)
    timezone = models.CharField(max_length=256, null=True, blank=True)
    created_by_email = models.CharField(max_length=256, null=True, blank=True)
    # channel posts / system posts
    channel = models.ForeignKey(
        "Channel", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=datetime.now)


class User(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    workspace = models.ForeignKey(
        "Workspace", on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(
        Event, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=256, null=True, blank=True)
    user_name = models.CharField(max_length=256, null=True, blank=True)
    user_email = models.CharField(max_length=256, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    select_date = models.DateTimeField(null=True, blank=True)
    date_end = models.DateTimeField(null=True, blank=True)
    link = models.CharField(max_length=256, null=True, blank=True)
    order = models.CharField(max_length=256, null=True, blank=True)
    status = models.CharField(max_length=256, null=True, blank=True)
    duration = models.CharField(max_length=256, null=True, blank=True)
    time_event = models.CharField(max_length=256, null=True, blank=True)
    comment = models.CharField(max_length=512, null=True, blank=True)
    company = models.CharField(max_length=256, null=True, blank=True)
    location = models.CharField(max_length=256, null=True, blank=True)
    reschedule_time = models.CharField(max_length=256, null=True, blank=True)
    reschedule_detail = models.CharField(max_length=256, null=True, blank=True)
    _event_id = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    timezone = models.CharField(max_length=256, null=True, blank=True)

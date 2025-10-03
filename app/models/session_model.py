from django.core.exceptions import ValidationError
from django.db import models
import uuid

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event = models.ForeignKey(
        'Event', on_delete=models.CASCADE, related_name='sessions')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    speaker = models.CharField(max_length=100, blank=True)
    track = models.ForeignKey(
        'Track', on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    capacity = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} - {self.event.title}"

    def clean(self):
        if self.track:
            conflicting_sessions = Session.objects.filter(
                track=self.track,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            ).exclude(id=self.id)

            if conflicting_sessions.exists():
                raise ValidationError(
                    "Schedule conflict with another session in the same track")

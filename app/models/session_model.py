from django.core.exceptions import ValidationError
from django.db import models
import uuid

class Session(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    speaker = models.CharField(max_length=100, blank=True)
    track = models.ForeignKey(
        'Track', on_delete=models.SET_NULL, null=True, blank=True, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['start_time']

    def __str__(self):
        return f"{self.title} - {self.track.name if self.track else 'No Track'} - {self.track.event.title if self.track and self.track.event else 'No Event'}"

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

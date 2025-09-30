from django.db import models
from django.utils import timezone
from datetime import datetime
from django.conf import settings
from django.contrib.auth.models import User


class Verification(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_query_name="verification"
    )
    verified = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    address = models.CharField(max_length=256, null=True, blank=True)
    code = models.CharField(max_length=256, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return 'Verification for: ' + self.user.first_name

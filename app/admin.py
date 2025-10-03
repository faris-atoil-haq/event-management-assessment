from django.contrib import admin
from app.models import *


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'user', 'status', 'date_start', 'date_end',
                    'capacity', 'attendee_count', 'created_at']
    list_filter = ['status', 'registration_open', 'created_at']
    search_fields = ['title', 'description', 'venue']
    readonly_fields = ['created_at', 'updated_at', 'attendee_count']

@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'session_count', 'created_at']
    list_filter = ['event']
    search_fields = ['name', 'description']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['title', 'track', 'speaker', 'start_time', 'end_time', 'created_at']
    list_filter = ['track', 'start_time']
    search_fields = ['title', 'speaker']
    
@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ['user', 'event', 'status', 'registration_date']
    list_filter = ['status', 'registration_date']
    search_fields = ['user__username', 'event__title']
    
@admin.register(Verification)
class VerificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'verified', 'admin', 'role', 'created_at']
    list_filter = ['verified', 'admin', 'role', 'created_at']
    search_fields = ['user__username', 'user__email', 'address', 'code']

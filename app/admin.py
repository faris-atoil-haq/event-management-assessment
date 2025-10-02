from django.contrib import admin
from app.models import *


class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'created_by', 'created_at', 'user', 'date_start', 'date_end', 'status']
    search_fields = ['id', 'title']
    date_hierarchy='created_at'
admin.site.register(Event, EventAdmin)

class VerificationAdmin(admin.ModelAdmin):
    list_display = ['verified', 'admin',
                    'user', 'created_at', 'address', 'code']
    search_fields = ['address']
    date_hierarchy='created_at'
admin.site.register(Verification, VerificationAdmin)

'''event_management/urls.py'''

from django.contrib import admin
from .views import index
from django.urls import path

        
# Main URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', index, name='index'),
]

# Error handlers
handler400 = 'event_management.views.handle_400'
handler404 = 'event_management.views.handle_404'
handler500 = 'event_management.views.handle_500'

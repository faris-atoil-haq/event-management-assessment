'''event_management/urls.py'''

from django.contrib import admin
from .views import landing_page
from django.urls import path, include

        
# Main URL patterns
urlpatterns = [
    path("admin/", admin.site.urls),
    path('app/', include('app.urls')),
    path('', landing_page, name='landing_page'),
]

# Error handlers
handler400 = 'event_management.views.handle_400'
handler404 = 'event_management.views.handle_404'
handler500 = 'event_management.views.handle_500'

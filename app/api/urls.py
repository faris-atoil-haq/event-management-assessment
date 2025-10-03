from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from app.api.views import (EventListView, MyEventsView, CustomTokenRefreshView,
                           CustomTokenObtainPairView, EventDetailView, 
                           register_to_event, user_profile)

urlpatterns = [
    # Authentication
    path('auth/login/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('auth/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),

    # User
    path('profile/', user_profile, name='user_profile'),

    # Events
    path('events/', EventListView.as_view(), name='event_list'),
    path('events/<int:pk>/', EventDetailView.as_view(), name='event_detail'),
    path('events/<int:event_id>/register/',
         register_to_event, name='register_event'),
    path('my-events/', MyEventsView.as_view(), name='my_events'),
]

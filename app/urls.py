from django.urls import path
from .views import (dashboard_content, events_table,
                    confirm, dashboard, create_and_manage_events,
                    signup, login_auth, signout)

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('dashboard_content/', dashboard_content, name='dashboard_content'),

    # Events URLs
    path('events/', dashboard, {'content_type': 'table'}, name='events'),
    path('events_table/', events_table, name='events_table'),

    # Management URLs
    path('manage_events/', dashboard,
         {'content_type': 'manage'}, name='manage_events'),
    path('manage_events/<uuid:id>/', create_and_manage_events,
         name='manage_event_detail'),
    path('create_events/', create_and_manage_events, name='create_events'),

    # Auth URLs
    path('signup/', signup, name='signup'),
    path('login/', login_auth, name='login'),
    path('confirm/', confirm, name='confirm'),
    path('signout/', signout, name='signout'),
]

# Error handlers
handler400 = 'event_management.views.handle_400'
handler404 = 'event_management.views.handle_404'
handler500 = 'event_management.views.handle_500'

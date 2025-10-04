from django.urls import path
from .views import (
    timeline,
     events_table,
     confirm, 
     dashboard, 
     create_and_manage_events,
     signup, 
     login_auth, 
     signout, 
     show_event_detail,
     manage_track,
     reset_password_email,
     reset_password,
     search_events
)
from .views.session_manager import (
     create_and_manage_session, 
     load_session,
     manage_track_session,
     session_list
)    
from .views.attendee_manager import (
     register_for_event, 
     cancel_registration, 
     attendee_list
)
from .views.documentation_view import documentation

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('timeline/', timeline, name='timeline'),

    # Events URLs
    path('remove_track/', manage_track, name='remove_track'),
    path('add_track/', manage_track, name='add_track'),
    path('events/', dashboard, {'content_type': 'table'}, name='events'),
    path('events_table/', events_table, name='events_table'),
    path('search_events/', search_events, name='search_events'),

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
    path('reset_password_email/', reset_password_email,
         name='reset_password_email'),
    path('reset_password/', reset_password, name='reset_password'),

    # Session Management URLs
    path('track/<uuid:track_id>/sessions/',
         session_list, name='session_list'),
    path('track/<uuid:track_id>/sessions/manage/',
         manage_track_session, name='manage_track_session'),
    path('session/manage/',
         create_and_manage_session, name='create_and_manage_session'),
    path('load_session/<uuid:session_id>/',
         load_session, name='load_session'),

    # Attendee Management URLs
    path('event/<uuid:event_id>/detail/',
         show_event_detail, name='show_event_detail'),
    path('event/<uuid:event_id>/register/',
         register_for_event, name='register_event'),
    path('event/<uuid:event_id>/cancel/',
         cancel_registration, name='cancel_registration'),
    path('event/<uuid:event_id>/attendees/',
         attendee_list, name='attendee_list'),
    
    # Documentation
    path('documentation/',
         documentation, name='documentation'),
]

# Error handlers
handler400 = 'event_management.views.handle_400'
handler404 = 'event_management.views.handle_404'
handler500 = 'event_management.views.handle_500'

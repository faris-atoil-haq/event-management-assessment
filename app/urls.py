from django.urls import path
from .views import confirm, event_input, dashboard, signup, login_auth, signout

app_name = 'app'

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('events/', event_input, name='event_input'),
    path('signup/', signup, name='signup'),
    path('login/', login_auth, name='login'),
    path('confirm/', confirm, name='confirm'),
    path('signout/', signout, name='signout'),
]

# Error handlers
handler400 = 'event_management.views.handle_400'
handler404 = 'event_management.views.handle_404'
handler500 = 'event_management.views.handle_500'

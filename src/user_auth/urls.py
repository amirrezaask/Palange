from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user_auth.views import SignupView, organizer_profile

app_name = 'auth'

urlpatterns = [
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignupView.as_view(), name='signup'),
    path('organizer_profile', organizer_profile, name='organizer_profile'),
    path('update_organizer_profile', update_organizer_profile, name="update_organizer_profile")
]

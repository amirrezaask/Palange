from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user_auth.views import SignupView, OrganizerProfileDetailView, EditOrganizerProfile

app_name = 'auth'

urlpatterns = [
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignupView.as_view(), name='signup'),
    path('organizer_profile/<int:pk>', OrganizerProfileDetailView.as_view(), name='organizer_profile'),
    path('update_organizer_profile/<int:pk>', EditOrganizerProfile.as_view(), name="update_organizer_profile")
]

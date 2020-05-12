from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from user_auth.views import SignupView

app_name = 'auth'

urlpatterns = [
    path('login', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignupView.as_view(), name='signup'),
]

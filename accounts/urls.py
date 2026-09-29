from django.contrib.auth.views import LoginView
from django.urls import path

from . import views

urlpatterns = [
    path("signup/", views.signup_view, name="signup"),
    path("login/", LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path("logout/", views.logout_view, name="logout"),
]
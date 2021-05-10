from .views import ChangePasswordView, LoginView, PasswordChangedView, RegisteredView, RegistrationView
from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

app_name = "urban_development"

urlpatterns = [
    url("login/", LoginView.as_view(), name="login_page"),
    url("register/", RegistrationView.as_view(), name="registration_page"),
    path("registered/", RegisteredView.as_view(), name="registered_page"),
    url("change_password/", ChangePasswordView.as_view(), name="change_password_page"),
    path("password_changed/", PasswordChangedView.as_view(), name="password_changed_page"),
    path("", RedirectView.as_view(url="login/", permanent=True)),
]

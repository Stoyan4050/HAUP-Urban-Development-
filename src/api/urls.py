from .views import ActivateAccountView, ChangePasswordView, LoginView, PasswordChangedView, RegistrationView, SendActivationEmailView
from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

app_name = "urban_development"

urlpatterns = [
    url("login/", LoginView.as_view(), name="login_page"),
    url("register/", RegistrationView.as_view(), name="registration_page"),
    path("send_activation_email/<slug:uid>/", SendActivationEmailView.as_view(), name="send_activation_email_page"),
    path("activate_account/<slug:uidb64>/<slug:token>/", ActivateAccountView.as_view(), name="activate_account_page"),
    url("change_password/", ChangePasswordView.as_view(), name="change_password_page"),
    path("password_changed/", PasswordChangedView.as_view(), name="password_changed_page"),
    path("", RedirectView.as_view(url="login/", permanent=True)),
]

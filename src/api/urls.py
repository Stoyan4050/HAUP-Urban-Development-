from .views import AccountActivatedView, ChangePasswordView, LoginView, PasswordChangedView, RegisterView, SendActivationEmailView, SendChangePasswordEmailView, MapInput
from django.urls import path
from django.views.generic import RedirectView

app_name = "urban_development"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login_page"),
    path("register/", RegisterView.as_view(), name="register_page"),
    path("send_activation_email/<slug:uid>/", SendActivationEmailView.as_view(), name="send_activation_email_page"),
    path("account_activated/<slug:uidb64>/<slug:token>/", AccountActivatedView.as_view(), name="account_activated_page"),
    path("change_password/", ChangePasswordView.as_view(), name="change_password_page"),
    path("send_change_password_email/<slug:uid>/", SendChangePasswordEmailView.as_view(), name="send_change_password_email_page"),
    path("password_changed/<slug:uidb64>/<slug:token>/", PasswordChangedView.as_view(), name="password_changed_page"),
    path("map_input/", MapInput.as_view(), name="map_input"),
    path("", RedirectView.as_view(url="login/", permanent=True)),
]

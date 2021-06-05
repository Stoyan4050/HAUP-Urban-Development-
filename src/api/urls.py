"""
urls.py
"""

from django.urls import path
from .views import AccountActivatedView, BaseView, ChangePasswordView, GetClassifiedAsView, GetClassifiedByView,\
    GetDataView, GuestView, LoginView, LogoutView, MapView, PasswordChangedView, RegisterView,\
    SendActivationEmailView, SendChangePasswordEmailView, HowToUseView

app_name = "urban_development"

urlpatterns = [
    path("", BaseView.as_view(),
         name="base_page"),
    path("guest/", GuestView.as_view(),
         name="guest_page"),
    path("login/", LoginView.as_view(),
         name="login_page"),
    path("logout/", LogoutView.as_view(),
         name="logout_page"),
    path("register/", RegisterView.as_view(),
         name="register_page"),
    path("send_activation_email/<slug:uid>/", SendActivationEmailView.as_view(),
         name="send_activation_email_page"),
    path("account_activated/<slug:uidb64>/<slug:token>/", AccountActivatedView.as_view(),
         name="account_activated_page"),
    path("change_password/", ChangePasswordView.as_view(),
         name="change_password_page"),
    path("send_change_password_email/<slug:uid>/", SendChangePasswordEmailView.as_view(),
         name="send_change_password_email_page"),
    path("password_changed/<slug:uidb64>/<slug:token>/", PasswordChangedView.as_view(),
         name="password_changed_page"),
    path("map/", MapView.as_view(),
         name="map_page"),
    path("get_classified_as/<parameters>/", GetClassifiedAsView.as_view(),
         name="get_classified_as_page"),
    path("get_classified_by/<parameters>/", GetClassifiedByView.as_view(),
         name="get_classified_by_page"),
    path("get_data/<parameters>/", GetDataView.as_view(),
         name="get_data_view"),
    path("how_to_use/", HowToUseView.as_view(),
         name="how_to_use")
]

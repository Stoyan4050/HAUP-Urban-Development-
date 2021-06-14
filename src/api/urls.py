"""
urls.py
"""

from django.urls import path
from .views import AccountActivatedView, BaseView, ChangePasswordView, GetClassifiedTilesView,\
    GuestView, LoginView, LogoutView, MainView, ManualClassificationView, PasswordChangedView, \
    RegisterView, SendActivationEmailView, SendChangePasswordEmailView, TransformCoordinatesView

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
    path("main/", MainView.as_view(),
         name="main_page"),
    path("get_classified_tiles/<parameters>/", GetClassifiedTilesView.as_view(),
         name="get_classified_tiles_page"),
    path("transform_coordinates/<parameters>/", TransformCoordinatesView.as_view(),
         name="transform_coordinates_page"),
    path("manual_classification/<parameters>/", ManualClassificationView.as_view(),
         name="manual_classification"),
]

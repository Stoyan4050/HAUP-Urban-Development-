"""
urls.py
"""

from django.urls import path
from api.views.account_activated_view import AccountActivatedView
from api.views.base_view import BaseView
from api.views.change_password_view import ChangePasswordView
from api.views.classify_tile_view import ClassifyTileView
from api.views.get_classified_tiles_view import GetClassifiedTilesView
from api.views.guest_view import GuestView
from api.views.login_view import LoginView
from api.views.logout_view import LogoutView
from api.views.main_view import MainView
from api.views.manual_classification_view import ManualClassificationView
from api.views.password_changed_view import PasswordChangedView
from api.views.register_view import RegisterView
from api.views.send_activation_email_view import SendActivationEmailView
from api.views.send_change_password_email_view import SendChangePasswordEmailView
from api.views.transform_coordinates_view import TransformCoordinatesView

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
         name="manual_classification_page"),
    path("classify_tile/<parameters>/", ClassifyTileView.as_view(),
         name="classify_tile_page"),
]

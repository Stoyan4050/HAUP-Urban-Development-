from . import views
from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

app_name = "urban_development"

urlpatterns = [
    url("login/", views.login_page, name="login_page"),
    url("register/", views.registration_page, name="registration_page"),
    path("registered/", views.registered_page, name="registered_page"),
    url("change_password/", views.change_password_page, name="change_password_page"),
    path("password_changed/", views.password_changed_page, name="password_changed_page"),
    path("", RedirectView.as_view(url="login/", permanent=True)),
]

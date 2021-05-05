from . import views
from django.conf.urls import url
from django.urls import path
from django.views.generic import RedirectView

app_name = "urban_development"

urlpatterns = [
    url("login/", views.login_page, name="login_page"),
    url("register/", views.registration_page, name="registration_page"),
    path("", RedirectView.as_view(url="login/", permanent=True)),
]

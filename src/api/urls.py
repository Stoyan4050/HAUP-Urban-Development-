from . import views
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', views.login_page, name='login_page'),
    path('', RedirectView.as_view(url='login/', permanent=True)),
]

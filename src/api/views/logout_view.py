"""
logout_view.py
"""

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class LogoutView(View):
    """
    class LogoutView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        logout(request)
        return redirect("urban_development:login_page")

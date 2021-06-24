"""
guest_view.py
"""

from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class GuestView(View):
    """
    class GuestView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        logout(request)
        return redirect("urban_development:main_page")

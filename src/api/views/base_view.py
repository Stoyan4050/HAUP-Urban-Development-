"""
base_view.py
"""

from django.shortcuts import redirect
from django.views import View


class BaseView(View):
    """
    class BaseView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        if request.user.is_authenticated:
            return redirect("urban_development:main_page")

        return redirect("urban_development:login_page")

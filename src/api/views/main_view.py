"""
main_view.py
"""

import collections
from django.shortcuts import render
from django.views import View
from api.utils.extract_available_years import extract_available_years


class MainView(View):
    """
    class MainView(View)
    """

    @staticmethod
    def get(request):
        """
        @staticmethod
        def get(request)
        """

        context = {
            "years": collections.OrderedDict(sorted(extract_available_years().items(), reverse=True)),
        }
        return render(request, "pages/main_page.html", context=context)

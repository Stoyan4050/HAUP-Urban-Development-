"""
login_view.py
"""

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View
from api.forms.login_form import LoginForm


class LoginView(View):
    """
    class LoginView(View)
    """

    _context = {
        "title": "Login Page",
        "action": "/urban_development/login/",
        "hyperlinks": {
            "Click here to change your password": "/urban_development/change_password/",
            "Click here to register": "/urban_development/register/",
            "Log in as a guest": "/urban_development/guest/",
        },
        "button": "Log in",
    }

    def get(self, request):
        """
        def get(self, request)
        """

        self._context["form"] = LoginForm()
        return render(request, "pages/login_page.html", context=self._context)

    def post(self, request):
        """
        def post(self, request)
        """

        form = LoginForm(data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            email = data.get("username")
            password = data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)
                return redirect("urban_development:main_page")

        self._context["form"] = form
        return render(request, "pages/login_page.html", context=self._context)

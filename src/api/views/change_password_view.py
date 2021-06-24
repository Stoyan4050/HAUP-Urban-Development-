"""
change_password_view.py
"""

from django.shortcuts import redirect, render
from django.views import View
from api.forms.change_password_form import ChangePasswordForm
from api.models.user import User


class ChangePasswordView(View):
    """
    class ChangePasswordView(View)
    """

    _context = {
        "title": "Change Password",
        "action": "/urban_development/change_password/",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }

    def get(self, request):
        """
        def get(self, request)
        """

        self._context["form"] = ChangePasswordForm()
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

    def post(self, request):
        """
        def post(self, request)
        """

        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)
            return redirect("urban_development:send_change_password_email_page", uid=user.id)

        self._context["form"] = form
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

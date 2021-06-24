"""
send_change_password_email_view.py
"""

from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.views import View
from api.utils.send_email import send_email


class SendChangePasswordEmailView(View):
    """
    class SendChangePasswordEmailView(View)
    """

    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request, uid):
        """
        def get(self, request, uid)
        """

        self._context["hyperlinks"] = {
            **{
                "Click here to resend the change password email":
                    "/urban_development/send_change_password_email/" + uid,
            },
            **self._context["hyperlinks"]
        }

        if send_email(uid, get_current_site(request).domain,
                      "Change the password for your Urban Development account.",
                      "pages/change_password_email.html"):
            self._context["title"] = "Change Password Email Sent"
            return render(request, "pages/register_and_change_password_page.html", context=self._context)

        self._context["title"] = "Change Password Email Not Sent"
        return render(request, "templates/user_data_template.html", context=self._context)

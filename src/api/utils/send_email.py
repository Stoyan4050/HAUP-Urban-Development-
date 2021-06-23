"""
send_email.py
"""

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from api.models.user import User
from api.tokens import TOKEN_GENERATOR


def send_email(uid, domain, email_subject, email_template):
    """
    def send_email(uid, domain, email_subject, email_template)
    """

    try:
        user = User.objects.get(pk=uid)
    except ObjectDoesNotExist:
        user = None

    if user is not None:
        email_message = render_to_string(email_template, {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": TOKEN_GENERATOR.make_token(user),
        })
        email = EmailMessage(email_subject, email_message, to=[user.email])
        email.send()
        return True

    return False

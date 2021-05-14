from .models import User
from .tokens import token_generator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

def send_email(uid, domain, email_subject, email_template):
    try:
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None:
        email_message = render_to_string(email_template, {
            "user": user,
            "domain": domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": token_generator.make_token(user),
        })
        email = EmailMessage(email_subject, email_message, to=[user.email])
        email.send()
        return True
    
    return False

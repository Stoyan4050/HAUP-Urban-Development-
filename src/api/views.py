from .forms import RegistrationForm, LoginForm, ChangePasswordForm
from .tokens import account_activation_token
from .models import User
from django.contrib.auth import authenticate, login
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

class LoginView(View):
    _context = {
        "title": "Login Page",
        "action": "login",
        "hyperlinks": {
            "Click here to change your password": "/urban_development/change_password/",
            "Click here to register": "/urban_development/register/",
            "Log in as a guest": "",
        },
        "button": "Log in",
    }

    def get(self, request):
        self._context["form"] = LoginForm()
        return render(request, "pages/login_page.html", context=self._context)
    
    def post(self, request):
        form = LoginForm(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            
            if user is not None:
                # login(request, user)
                return redirect("urban_development:registration_page")
        
        self._context["form"] = form
        return render(request, "pages/login_page.html", context=self._context)

class RegistrationView(View):
    _context = {
        "title": "Registration Page",
        "action": "register",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Register",
    }

    def get(self, request):
        self._context["form"] = RegistrationForm()
        return render(request, "pages/registration_and_change_password_page.html", context=self._context)

    def post(self, request):
        form = RegistrationForm(data=request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect("urban_development:send_activation_email_page", uid=user.id)
        
        self._context["form"] = form
        return render(request, "pages/registration_and_change_password_page.html", context=self._context)

class SendActivationEmailView(View):
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        } ,
    }

    def get(self, request, uid):
        self._context["hyperlinks"] = {**{"Click here to resend the activation email": "/urban_development/send_activation_email/" + uid}, **self._context["hyperlinks"]}
        
        try:
            user = User.objects.get(pk=uid)
        except:
            user = None

        if user is not None:
            current_site = get_current_site(request)
            email_subject = "Activate your Urban Devlopment account."
            email_message = render_to_string("pages/account_activation_email.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            })
            email_to = user.email
            email = EmailMessage(email_subject, email_message, to=[email_to])
            email.send()
            self._context["title"] = "Activation Email Sent"
            return render(request, "pages/registration_and_change_password_page.html", context=self._context)
        else:
            self._context["title"] = "Activation Email Not Sent"
            return render(request, "templates/user_data_template.html", context=self._context)

class ActivateAccountView(View):
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            self._context["title"] = "Account Activated Successfully"
            return render(request, "templates/user_data_template.html", context=self._context)
        else:
            self._context["title"] = "Invalid Activation Link"
            return render(request, "templates/user_data_template.html", context=self._context)

class ChangePasswordView(View):
    _context = {
        "title": "Change Password",
        "action": "change_password",
        "hyperlinks": {
            "Click here to register": "urban_development/register/",
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }

    def get(self, request):
        self._context["form"] = ChangePasswordForm()
        return render(request, "pages/registration_and_change_password_page.html", context=self._context)

    def post(self, request):
        form = ChangePasswordForm(data=request.POST)
        
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data['password1']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return redirect("urban_development:password_changed_page")

        self._context["form"] = form
        return render(request, "pages/registration_and_change_password_page.html", context=self._context)

class PasswordChangedView(View):
    _context = {
        "title": "Password Changed",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request):
        return render(request, "templates/user_data_template.html", context=self._context)

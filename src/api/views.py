from .email import send_email
from .forms import ChangePasswordForm, RegisterForm, LoginForm, NewPasswordForm
from .models import User, Tile, Classification
from .tokens import token_generator
from django.contrib.auth import authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.views import View

class LoginView(View):
    _context = {
        "title": "Login Page",
        "action": "/urban_development/login/",
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
                return redirect("urban_development:register_page")
        
        self._context["form"] = form
        return render(request, "pages/login_page.html", context=self._context)

class RegisterView(View):
    _context = {
        "title": "Registration Page",
        "action": "/urban_development/register/",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Register",
    }

    def get(self, request):
        self._context["form"] = RegisterForm()
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

    def post(self, request):
        form = RegisterForm(data=request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            return redirect("urban_development:send_activation_email_page", uid=user.id)
        
        self._context["form"] = form
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

class SendActivationEmailView(View):
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        } ,
    }

    def get(self, request, uid):
        self._context["hyperlinks"] = {**{"Click here to resend the activation email": "/urban_development/send_activation_email/" + uid}, **self._context["hyperlinks"]}

        if send_email(uid, get_current_site(request).domain, "Activate your Urban Development account.", "pages/account_activation_email.html"):
            self._context["title"] = "Activation Email Sent"
            return render(request, "pages/register_and_change_password_page.html", context=self._context)

        self._context["title"] = "Activation Email Not Sent"
        return render(request, "templates/user_data_template.html", context=self._context)

class AccountActivatedView(View):
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

        if user is not None and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            self._context["title"] = "Account Activated Successfully"
            return render(request, "templates/user_data_template.html", context=self._context)
    
        self._context["title"] = "Invalid Activation Link"
        return render(request, "templates/user_data_template.html", context=self._context)

class ChangePasswordView(View):
    _context = {
        "title": "Change Password",
        "action": "/urban_development/change_password/",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }

    def get(self, request):
        self._context["form"] = ChangePasswordForm()
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data.get("email")
            user = User.objects.get(email=email)
            return redirect("urban_development:send_change_password_email_page", uid=user.id)

        self._context["form"] = form
        return render(request, "pages/register_and_change_password_page.html", context=self._context)

class SendChangePasswordEmailView(View):
    _context = {
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        } ,
    }

    def get(self, request, uid):
        self._context["hyperlinks"] = {**{"Click here to resend the change password email": "/urban_development/send_change_password_email/" + uid}, **self._context["hyperlinks"]}

        if send_email(uid, get_current_site(request).domain, "Change the password for your Urban Development account.", "pages/change_password_email.html"):
            self._context["title"] = "Change Password Email Sent"
            return render(request, "pages/register_and_change_password_page.html", context=self._context)
        
        self._context["title"] = "Change Password Email Not Sent"
        return render(request, "templates/user_data_template.html", context=self._context)

class PasswordChangedView(View):
    _form_context = {
        "title": "Change password",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }
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
    
        if user is not None and token_generator.check_token(user, token):
            form = NewPasswordForm(user=user)
            self._form_context["form"] = form
            self._form_context["action"] = "/urban_development/password_changed/" + uidb64 + "/" + token + "/"
            return render(request, "pages/register_and_change_password_page.html", context=self._form_context)
    
        self._context["title"] = "Password Not Changed"
        return render(request, "templates/user_data_template.html", context=self._context)

    def post(self, request, uidb64, token):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            form = NewPasswordForm(data=request.POST, user=user)

            if form.is_valid():
                new_password = form.cleaned_data.get("new_password1")
                user.set_password(new_password)
                user.save()
                self._context["title"] = "Password Changed Successfully"
                return render(request, "templates/user_data_template.html", context=self._context)
            else:
                self._form_context["form"] = form
                self._form_context["action"] = "/urban_development/password_changed/" + uidb64 + "/" + token + "/"
                return render(request, "pages/register_and_change_password_page.html", context=self._form_context)

        self._context["title"] = "Password Not Changed"
        return render(request, "templates/user_data_template.html", context=self._context)

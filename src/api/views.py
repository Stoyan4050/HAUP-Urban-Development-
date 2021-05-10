from .forms import RegistrationForm, LoginForm, ChangePasswordForm
from .models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
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
            user = form.save()
            return redirect("urban_development:registered_page")
        
        self._context["form"] = form
        return render(request, "pages/registration_and_change_password_page.html", context=self._context)

class RegisteredView(View):
    _context = {
        "title": "Account Created",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }

    def get(self, request):
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

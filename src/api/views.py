from .forms import RegistrationForm, LoginForm, ChangePasswordForm
from .models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render

def login_page(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)
            if user is not None:
                # login(request, user)
                return redirect("urban_development:registration_page")
    else:
        form = LoginForm()
    context = {
        "title": "Login Page",
        "action": "login",
        "form": form,
        "hyperlinks": {
            "Click here to change your password": "/urban_development/change_password/",
            "Click here to register": "/urban_development/register/",
            "Log in as a guest": "",
        },
        "button": "Log in",
    }
    return render(request, "pages/login_page.html", context=context)

def registration_page(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            return redirect("urban_development:registered_page")
    else:
        form = RegistrationForm()
    context = {
        "title": "Registration Page",
        "action": "register",
        "form": form,
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Register",
    }
    return render(request, "pages/registration_and_change_password_page.html", context=context)

def registered_page(request):
    context = {
        "title": "Account Created",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }
    return render(request, "templates/user_data_template.html", context=context)

def change_password_page(request):
    if request.method == "POST":
        form = ChangePasswordForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data['password1']
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            return redirect("urban_development:password_changed_page")
    else:
        form = ChangePasswordForm()
    context = {
        "title": "Change Password",
        "action": "change_password",
        "form": form,
        "hyperlinks": {
            "Click here to register": "urban_development/register/",
            "Click here to log in": "/urban_development/login/",
        },
        "button": "Change Password",
    }
    return render(request, "pages/registration_and_change_password_page.html", context=context)

def password_changed_page(request):
    context = {
        "title": "Password Changed",
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
    }
    return render(request, "templates/user_data_template.html", context=context)

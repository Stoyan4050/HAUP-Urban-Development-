from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm, LoginForm
from django.shortcuts import redirect
from django.contrib import messages

def login_page(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
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
            "Click here to change your password": "",
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
            # login(request, user)
            return redirect("urban_development:login_page")
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
    return render(request, "pages/registration_page.html", context=context)

from django.shortcuts import render
from django.contrib.auth import login, authenticate
from .forms import RegistrationForm
from django.shortcuts import redirect
from django.contrib import messages

def login_page(request):
    context = {
        "title": "Login Page",
        "inputs": {
            "Email": False, 
            "Password": True,
        },
        "hyperlinks": {
            "Click here to register": "/urban_development/register/",
            "Log in as a guest": "",
        },
        "button" : "Log in",
    }
    return render(request, 'pages/login_registration_page.html', context=context)

def registration_page(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)
            return redirect('urban_development:login_page')
    else:
        form = RegistrationForm()
    context = {
        "title": "Registration Page",
        "form": form,
        "hyperlinks": {
        "Click here to log in": "/urban_development/login/",
        },
        "button" : "Register",
    }
    return render(request, 'pages/login_registration_page.html', context=context)

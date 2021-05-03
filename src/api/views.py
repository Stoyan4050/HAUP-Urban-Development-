from django.shortcuts import render

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
    context = {
        "title": "Registration Page",
        "inputs": {
            "Email": False,
            "First name": False,
            "Last name": False,
            "Username": False,
            "Password": True,
            "Confirm password": True,
        },
        "hyperlinks": {
            "Click here to log in": "/urban_development/login/",
        },
        "button" : "Register",
    }
    return render(request, 'pages/login_registration_page.html', context=context)

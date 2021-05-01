from django.shortcuts import render

def login_page(request):
    return render(request, 'pages/login_page.html')

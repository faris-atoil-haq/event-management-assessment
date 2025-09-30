from django.shortcuts import render

# Create your views here.

def index(request, public=True):
    return render(request, 'index.html', {'public': public})

def login(request):
    return render(request, 'login_page.html')


def event_input(request):
    return render(request, 'event_input.html')

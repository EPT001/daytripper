# views.py

from django.shortcuts import render

from daytripper import myapp

def index(request):
    return render(request, 'myapp/index.html')

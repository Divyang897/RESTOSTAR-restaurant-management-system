from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

def login_view(request):
    # your login logic
    return render(request, 'users/login.html')


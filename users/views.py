from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.models import User

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # find username using email (Django login needs username)
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            messages.error(request, "No user found with this email.")
            return render(request, 'users/login.html')

        # authenticate user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome {user.username}!")
            return redirect('/dashboard/')  # Redirect to Django admin
        else:
            messages.error(request, "Invalid password. Please try again.")

    return render(request, 'users/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')
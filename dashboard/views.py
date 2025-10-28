from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required  # ✅ Django will use LOGIN_URL from settings.py
def dashboard(request):
    return render(request, 'dashboard/dashboard_home.html')
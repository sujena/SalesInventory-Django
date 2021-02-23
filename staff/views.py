from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render(request, 'staff/home.html')


@login_required
def dashboard(request):
    return render(request, 'system/dashboard.html')






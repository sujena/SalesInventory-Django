from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='staff-home'),
    path('login/', auth_views.LoginView.as_view(template_name='staff/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='staff/logout.html'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('report/', views.generate_view, name='report'),
]

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
    path('profile/', views.profile, name='profile'),
    path('password-reset/'
         , auth_views.PasswordResetView.as_view(template_name='staff/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/'
         , auth_views.PasswordResetDoneView.as_view(template_name='staff/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/'
         , auth_views.PasswordResetConfirmView.as_view(template_name='staff/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete'
         , auth_views.PasswordResetCompleteView.as_view(template_name='staff/password_reset_complete.html'),
         name='password_reset_complete'),
]

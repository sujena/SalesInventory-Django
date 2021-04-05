from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
    path('listItems/', views.list_items, name='inventory-items'),
    path('transaction/', views.transaction, name='transaction'),
    path('submitDetails/', views.submitDetails, name='submitDetails'),
    path('savePurchaseDetails/', views.savePurchaseDetails, name='savePurchaseDetails'),

]



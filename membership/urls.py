from django.urls import path
from membership.views import CustomerCreateView

urlpatterns = [
    path('membership/', CustomerCreateView.as_view(), name='membership'),
]

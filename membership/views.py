from django.shortcuts import render
from django.views.generic import CreateView
from .models import Customer
from .forms import CustomerForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.


@method_decorator(login_required, name='dispatch')
class CustomerCreateView(CreateView):
    model = Customer
    form_class = CustomerForm
    template_name = 'system/customer_form.html'

    #fields = ('first_name', 'last_name', 'address', 'phone','email')

'''
class CustomerDetailView(DetailView):
    model=Customer
'''
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


class Customer(models.Model):
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    address=models.CharField(max_length=254, blank=True)
    phone=models.CharField(max_length=10, unique=True)
    email=models.EmailField(max_length=254)
    created_by= models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created= models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        #"Returns the person's full name."
        return '%s %s' % (self.first_name, self.last_name)

    def __str__(self):
        return self.full_name

    def get_absolute_url(self):
        return reverse('membership')
